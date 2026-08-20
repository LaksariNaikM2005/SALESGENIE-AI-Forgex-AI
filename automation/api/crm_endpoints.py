from datetime import datetime, timezone
from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request

from backend.database import (
    Activity,
    FollowUp,
    Lead,
    Meeting,
    Notification,
    close_session,
    get_session,
)

# Blueprint requested name
automation_bp = Blueprint("automation_bp", __name__)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Require that an authentication mechanism has set g.current_user.
        # This keeps the endpoint "authenticated" while deferring auth implementation
        # to the application's existing middleware.
        user = getattr(g, "current_user", None)
        if not user:
            return jsonify({"success": False, "message": "Authentication required"}), 401
        return f(*args, **kwargs)

    return decorated


def _parse_datetime(val: str | None) -> datetime | None:
    if not val:
        return None
    try:
        dt = datetime.fromisoformat(val)
    except Exception:
        # fallback: try to parse as naive and assume UTC
        try:
            dt = datetime.strptime(val, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            raise
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _serialize_followup(f: FollowUp) -> dict:
    return {
        "id": f.id,
        "lead_id": f.lead_id,
        "due_at": f.due_at.isoformat() if f.due_at else None,
        "priority": f.priority,
        "status": f.status,
        "notes": f.notes,
        "created_at": f.created_at.isoformat() if f.created_at else None,
        "completed_at": f.completed_at.isoformat() if getattr(f, "completed_at", None) else None,
    }


def _serialize_meeting(m: Meeting) -> dict:
    return {
        "id": m.id,
        "lead_id": m.lead_id,
        "title": m.title,
        "scheduled_at": m.scheduled_at.isoformat() if m.scheduled_at else None,
        "status": m.status,
        "notes": m.notes,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    }


def _serialize_activity(a: Activity) -> dict:
    return {
        "id": a.id,
        "lead_id": a.lead_id,
        "activity_type": a.activity_type,
        "description": a.description,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


def _serialize_notification(n: Notification) -> dict:
    return {
        "id": n.id,
        "lead_id": n.lead_id,
        "message": n.message,
        "notification_type": n.notification_type,
        "is_read": bool(n.is_read),
        "created_at": n.created_at.isoformat() if n.created_at else None,
    }


# Follow-ups
@automation_bp.route("/api/follow-ups", methods=["POST"])
@require_auth
def create_follow_up():
    payload = request.get_json() or {}
    lead_id = payload.get("lead_id")
    if lead_id is None:
        return jsonify({"success": False, "message": "lead_id is required"}), 400

    session = get_session()
    try:
        lead = session.get(Lead, lead_id)
        if not lead:
            return jsonify({"success": False, "message": "Lead not found"}), 404

        due_at = _parse_datetime(payload.get("due_at"))
        follow = FollowUp(
            lead_id=lead_id,
            due_at=due_at if due_at is not None else datetime.now(timezone.utc),
            priority=payload.get("priority", "Normal"),
            status=payload.get("status", "Pending"),
            notes=payload.get("notes", ""),
        )
        session.add(follow)
        session.commit()
        session.refresh(follow)
        return jsonify({"success": True, "message": "Follow-up created", "data": _serialize_followup(follow)})
    except Exception as exc:  # pragma: no cover - top-level safety
        session.rollback()
        current_app.logger.exception("Error creating follow-up")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            # remove scoped session if the app expects it
            try:
                close_session(None)
            except Exception:
                pass


@automation_bp.route("/api/follow-ups", methods=["GET"])
@require_auth
def list_follow_ups():
    session = get_session()
    try:
        # Optionally support filtering by lead_id
        lead_id = request.args.get("lead_id", type=int)
        q = session.query(FollowUp)
        if lead_id:
            q = q.filter(FollowUp.lead_id == lead_id)
        followups = q.all()
        data = [_serialize_followup(f) for f in followups]
        return jsonify({"success": True, "message": "Follow-ups retrieved", "data": data})
    except Exception as exc:
        current_app.logger.exception("Error listing follow-ups")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            try:
                close_session(None)
            except Exception:
                pass


@automation_bp.route("/api/follow-ups/<int:item_id>", methods=["PUT"])
@require_auth
def update_follow_up(item_id: int):
    payload = request.get_json() or {}
    session = get_session()
    try:
        follow = session.get(FollowUp, item_id)
        if not follow:
            return jsonify({"success": False, "message": "Follow-up not found"}), 404

        # allow updating certain fields
        if "lead_id" in payload:
            new_lead_id = payload.get("lead_id")
            if not session.get(Lead, new_lead_id):
                return jsonify({"success": False, "message": "Lead not found"}), 404
            follow.lead_id = new_lead_id
        if "due_at" in payload:
            follow.due_at = _parse_datetime(payload.get("due_at"))
        if "priority" in payload:
            follow.priority = payload.get("priority")
        if "status" in payload:
            follow.status = payload.get("status")
        if "notes" in payload:
            follow.notes = payload.get("notes")

        session.add(follow)
        session.commit()
        session.refresh(follow)
        return jsonify({"success": True, "message": "Follow-up updated", "data": _serialize_followup(follow)})
    except Exception as exc:
        session.rollback()
        current_app.logger.exception("Error updating follow-up")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            try:
                close_session(None)
            except Exception:
                pass


@automation_bp.route("/api/follow-ups/<int:item_id>/complete", methods=["POST"])
@require_auth
def complete_follow_up(item_id: int):
    session = get_session()
    try:
        follow = session.get(FollowUp, item_id)
        if not follow:
            return jsonify({"success": False, "message": "Follow-up not found"}), 404

        follow.status = "Completed"
        follow.completed_at = datetime.now(timezone.utc)
        session.add(follow)
        session.commit()
        session.refresh(follow)
        return jsonify({"success": True, "message": "Follow-up completed", "data": _serialize_followup(follow)})
    except Exception as exc:
        session.rollback()
        current_app.logger.exception("Error completing follow-up")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            try:
                close_session(None)
            except Exception:
                pass


# Meetings
@automation_bp.route("/api/meetings", methods=["POST"])
@require_auth
def create_meeting():
    payload = request.get_json() or {}
    lead_id = payload.get("lead_id")
    if lead_id is None:
        return jsonify({"success": False, "message": "lead_id is required"}), 400

    session = get_session()
    try:
        lead = session.get(Lead, lead_id)
        if not lead:
            return jsonify({"success": False, "message": "Lead not found"}), 404

        scheduled_at = _parse_datetime(payload.get("scheduled_at"))
        meeting = Meeting(
            lead_id=lead_id,
            title=payload.get("title", ""),
            scheduled_at=scheduled_at if scheduled_at is not None else datetime.now(timezone.utc),
            status=payload.get("status", "Scheduled"),
            notes=payload.get("notes", ""),
        )
        session.add(meeting)
        session.commit()
        session.refresh(meeting)
        return jsonify({"success": True, "message": "Meeting created", "data": _serialize_meeting(meeting)})
    except Exception as exc:
        session.rollback()
        current_app.logger.exception("Error creating meeting")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            try:
                close_session(None)
            except Exception:
                pass


@automation_bp.route("/api/meetings", methods=["GET"])
@require_auth
def list_meetings():
    session = get_session()
    try:
        lead_id = request.args.get("lead_id", type=int)
        q = session.query(Meeting)
        if lead_id:
            q = q.filter(Meeting.lead_id == lead_id)
        meetings = q.all()
        data = [_serialize_meeting(m) for m in meetings]
        return jsonify({"success": True, "message": "Meetings retrieved", "data": data})
    except Exception as exc:
        current_app.logger.exception("Error listing meetings")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            try:
                close_session(None)
            except Exception:
                pass


@automation_bp.route("/api/meetings/<int:item_id>", methods=["PUT"])
@require_auth
def update_meeting(item_id: int):
    payload = request.get_json() or {}
    session = get_session()
    try:
        meeting = session.get(Meeting, item_id)
        if not meeting:
            return jsonify({"success": False, "message": "Meeting not found"}), 404

        if "lead_id" in payload:
            new_lead_id = payload.get("lead_id")
            if not session.get(Lead, new_lead_id):
                return jsonify({"success": False, "message": "Lead not found"}), 404
            meeting.lead_id = new_lead_id
        if "title" in payload:
            meeting.title = payload.get("title")
        if "scheduled_at" in payload:
            meeting.scheduled_at = _parse_datetime(payload.get("scheduled_at"))
        if "status" in payload:
            meeting.status = payload.get("status")
        if "notes" in payload:
            meeting.notes = payload.get("notes")

        session.add(meeting)
        session.commit()
        session.refresh(meeting)
        return jsonify({"success": True, "message": "Meeting updated", "data": _serialize_meeting(meeting)})
    except Exception as exc:
        session.rollback()
        current_app.logger.exception("Error updating meeting")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            try:
                close_session(None)
            except Exception:
                pass


# Activities
@automation_bp.route("/api/activities", methods=["GET"])
@require_auth
def list_activities():
    session = get_session()
    try:
        lead_id = request.args.get("lead_id", type=int)
        q = session.query(Activity)
        if lead_id:
            q = q.filter(Activity.lead_id == lead_id)
        activities = q.all()
        data = [_serialize_activity(a) for a in activities]
        return jsonify({"success": True, "message": "Activities retrieved", "data": data})
    except Exception as exc:
        current_app.logger.exception("Error listing activities")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            try:
                close_session(None)
            except Exception:
                pass


# Notifications
@automation_bp.route("/api/notifications", methods=["GET"])
@require_auth
def list_notifications():
    session = get_session()
    try:
        lead_id = request.args.get("lead_id", type=int)
        q = session.query(Notification)
        if lead_id:
            q = q.filter(Notification.lead_id == lead_id)
        notifications = q.all()
        data = [_serialize_notification(n) for n in notifications]
        return jsonify({"success": True, "message": "Notifications retrieved", "data": data})
    except Exception as exc:
        current_app.logger.exception("Error listing notifications")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            try:
                close_session(None)
            except Exception:
                pass


@automation_bp.route("/api/notifications/<int:item_id>/read", methods=["POST"])
@require_auth
def mark_notification_read(item_id: int):
    session = get_session()
    try:
        n = session.get(Notification, item_id)
        if not n:
            return jsonify({"success": False, "message": "Notification not found"}), 404
        n.is_read = True
        session.add(n)
        session.commit()
        session.refresh(n)
        return jsonify({"success": True, "message": "Notification marked read", "data": _serialize_notification(n)})
    except Exception as exc:
        session.rollback()
        current_app.logger.exception("Error marking notification read")
        return jsonify({"success": False, "message": str(exc)}), 500
    finally:
        try:
            session.close()
        finally:
            try:
                close_session(None)
            except Exception:
                pass
