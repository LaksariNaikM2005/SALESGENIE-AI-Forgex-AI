from datetime import datetime, timedelta, timezone

import schedule

from backend.database import (
    Activity,
    FollowUp,
    Lead,
    Meeting,
    Notification,
    get_session,
)


def check_due_followups():
    """Create notifications for pending follow-ups that are due."""
    session = get_session()

    try:
        now = datetime.now(timezone.utc)

        followups = (
            session.query(FollowUp)
            .filter(
                FollowUp.status != "Completed",
                FollowUp.due_at <= now,
            )
            .all()
        )

        created = 0

        for followup in followups:
            existing = (
                session.query(Notification)
                .filter(
                    Notification.lead_id == followup.lead_id,
                    Notification.notification_type == "follow_up",
                    Notification.message.like(f"%follow-up #{followup.id}%"),
                )
                .first()
            )

            if existing:
                continue

            notification = Notification(
                lead_id=followup.lead_id,
                message=f"Follow-up #{followup.id} is due.",
                notification_type="follow_up",
                is_read=False,
                created_at=now,
            )

            session.add(notification)
            created += 1

        session.commit()

        return {
            "success": True,
            "checked": len(followups),
            "notifications_created": created,
        }

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def check_upcoming_meetings():
    """Create notifications for meetings scheduled within 24 hours."""
    session = get_session()

    try:
        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(hours=24)

        meetings = (
            session.query(Meeting)
            .filter(
                Meeting.scheduled_at >= now,
                Meeting.scheduled_at <= tomorrow,
                Meeting.status != "Cancelled",
            )
            .all()
        )

        created = 0

        for meeting in meetings:
            existing = (
                session.query(Notification)
                .filter(
                    Notification.lead_id == meeting.lead_id,
                    Notification.notification_type == "meeting",
                    Notification.message.like(f"%meeting #{meeting.id}%"),
                )
                .first()
            )

            if existing:
                continue

            notification = Notification(
                lead_id=meeting.lead_id,
                message=f"Upcoming meeting #{meeting.id}.",
                notification_type="meeting",
                is_read=False,
                created_at=now,
            )

            session.add(notification)
            created += 1

        session.commit()

        return {
            "success": True,
            "checked": len(meetings),
            "notifications_created": created,
        }

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def create_notifications():
    """Run all notification checks."""
    return {
        "followups": check_due_followups(),
        "meetings": check_upcoming_meetings(),
    }


def generate_daily_report():
    """Generate a daily sales summary without modifying lead data."""
    session = get_session()

    try:
        today = datetime.now(timezone.utc).date()

        leads = session.query(Lead).all()

        total_leads = len(leads)

        new_leads = sum(
            1
            for lead in leads
            if lead.created_at and lead.created_at.date() == today
        )

        hot_leads = sum(
            1 for lead in leads
            if (lead.category or "").lower() == "hot"
        )

        closed_won = sum(
            1 for lead in leads
            if (lead.stage or "").lower() == "closed won"
        )

        pipeline_value = sum(
            float(lead.revenue or 0)
            for lead in leads
        )

        completed_followups = (
            session.query(FollowUp)
            .filter(FollowUp.status == "Completed")
            .count()
        )

        upcoming_meetings = (
            session.query(Meeting)
            .filter(
                Meeting.scheduled_at >= datetime.now(timezone.utc),
                Meeting.status != "Cancelled",
            )
            .count()
        )

        return {
            "date": today.isoformat(),
            "total_leads": total_leads,
            "new_leads": new_leads,
            "hot_leads": hot_leads,
            "closed_won_leads": closed_won,
            "pipeline_value": round(pipeline_value, 2),
            "completed_followups": completed_followups,
            "upcoming_meetings": upcoming_meetings,
        }

    finally:
        session.close()



def process_due_emails():
    """Process scheduled emails that are due for delivery."""
    import os
    import smtplib
    from email.message import EmailMessage

    from backend.database import Email, get_session

    session = get_session()
    results = {
        "checked": 0,
        "sent": 0,
        "pending": 0,
        "failed": 0,
    }

    try:
        now = datetime.now(timezone.utc)

        emails = (
            session.query(Email)
            .filter(
                Email.status == "scheduled",
                Email.scheduled_at <= now,
            )
            .all()
        )

        results["checked"] = len(emails)

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port_raw = os.getenv("SMTP_PORT", "587")
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        smtp_from = os.getenv("SMTP_FROM_EMAIL")
        smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in {
            "1", "true", "yes", "on"
        }

        try:
            smtp_port = int(smtp_port_raw)
        except (TypeError, ValueError):
            smtp_port = 587

        smtp_available = bool(
            smtp_host and smtp_port and smtp_username and
            smtp_password and smtp_from
        )

        for email_record in emails:
            try:
                if not smtp_available:
                    email_record.status = "pending"
                    email_record.error_message = (
                        "SMTP configuration is incomplete. "
                        "Configure SMTP_HOST, SMTP_PORT, SMTP_USERNAME, "
                        "SMTP_PASSWORD and SMTP_FROM_EMAIL."
                    )
                    results["pending"] += 1
                    session.commit()
                    continue

                message = EmailMessage()
                message["From"] = smtp_from
                message["To"] = email_record.recipient
                message["Subject"] = email_record.subject
                message.set_content(email_record.body)

                with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
                    if smtp_use_tls:
                        server.starttls()

                    server.login(smtp_username, smtp_password)
                    server.send_message(message)

                email_record.status = "sent"
                email_record.sent_at = now
                email_record.error_message = None

                session.commit()
                results["sent"] += 1

            except Exception as exc:
                session.rollback()

                failed_email = session.get(Email, email_record.id)
                if failed_email:
                    failed_email.status = "failed"
                    failed_email.error_message = str(exc)[:2000]
                    session.commit()

                results["failed"] += 1

        return {
            "success": True,
            **results,
        }

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()
def run_scheduled_tasks():
    """Run the complete automation cycle."""
    notifications = create_notifications()
    report = generate_daily_report()
    emails = process_due_emails()

    return {
        "success": True,
        "notifications": notifications,
        "daily_report": report,
    }


def start_scheduler():
    """Configure the background automation scheduler."""
    schedule.every(30).minutes.do(create_notifications)
    schedule.every().day.at("18:00").do(generate_daily_report)

    return schedule


if __name__ == "__main__":
    start_scheduler()

    while True:
        schedule.run_pending()
