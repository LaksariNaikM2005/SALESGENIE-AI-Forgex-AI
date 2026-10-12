import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { User, Mail, Shield, Key, CheckCircle, AlertCircle, Save, Calendar } from 'lucide-react';

const Profile = () => {
  const { user, updateProfile, changePassword } = useContext(AuthContext);

  // Profile form state
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [profileMsg, setProfileMsg] = useState('');
  const [profileErr, setProfileErr] = useState('');
  const [profileLoading, setProfileLoading] = useState(false);

  // Password form state
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [pwdMsg, setPwdMsg] = useState('');
  const [pwdErr, setPwdErr] = useState('');
  const [pwdLoading, setPwdLoading] = useState(false);

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setProfileMsg('');
    setProfileErr('');
    setProfileLoading(true);

    try {
      await updateProfile({ name, email });
      setProfileMsg('Profile updated successfully!');
    } catch (err) {
      setProfileErr(err.response?.data?.error || 'Failed to update profile');
    } finally {
      setProfileLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPwdMsg('');
    setPwdErr('');

    if (newPassword !== confirmPassword) {
      setPwdErr('New passwords do not match');
      return;
    }

    if (newPassword.length < 8) {
      setPwdErr('New password must be at least 8 characters long');
      return;
    }

    setPwdLoading(true);

    try {
      await changePassword(currentPassword, newPassword, confirmPassword);
      setPwdMsg('Password changed successfully!');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err) {
      setPwdErr(err.response?.data?.error || 'Failed to change password');
    } finally {
      setPwdLoading(false);
    }
  };

  return (
    <div className="container-fluid p-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div>
          <h2 className="fw-bold text-light mb-1">User Profile & Account Settings</h2>
          <p className="small mb-0" style={{ color: '#cbd5e1' }}>Manage your account information, security credentials, and preferences</p>
        </div>
      </div>

      <div className="row g-4">
        {/* User Identity Card */}
        <div className="col-lg-4">
          <div className="card bg-dark border-secondary p-4 text-light h-100">
            <div className="text-center mb-4">
              <div
                className="rounded-circle bg-primary d-inline-flex align-items-center justify-content-center mb-3 shadow"
                style={{ width: '80px', height: '80px', fontSize: '32px', fontWeight: 'bold' }}
              >
                {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
              </div>
              <h4 className="fw-bold mb-1">{user?.name}</h4>
              <p className="small mb-2" style={{ color: '#cbd5e1' }}>{user?.email}</p>
              <span className="badge bg-primary text-capitalize px-3 py-2">
                <Shield size={14} className="me-1" />
                {user?.role?.replace('_', ' ')}
              </span>
            </div>

            <hr className="border-secondary" />

            <div className="vstack gap-3 small">
              <div className="d-flex align-items-center justify-content-between">
                <span style={{ color: '#cbd5e1' }}>Account Status:</span>
                <span className={`badge ${user?.is_active ? 'bg-success' : 'bg-danger'}`}>
                  {user?.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className="d-flex align-items-center justify-content-between">
                <span style={{ color: '#cbd5e1' }}><Calendar size={14} className="me-1" /> Member Since:</span>
                <span className="text-light">{user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</span>
              </div>
              <div className="d-flex align-items-center justify-content-between">
                <span style={{ color: '#cbd5e1' }}>Last Active Login:</span>
                <span className="text-light">{user?.last_login_at ? new Date(user.last_login_at).toLocaleString() : 'Just now'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Profile Information Form */}
        <div className="col-lg-8">
          <div className="card bg-dark border-secondary p-4 text-light mb-4">
            <h5 className="fw-bold mb-3 d-flex align-items-center gap-2">
              <User className="text-primary" size={20} />
              Profile Details
            </h5>

            {profileMsg && <div className="alert alert-success p-2 small d-flex align-items-center gap-2"><CheckCircle size={16} />{profileMsg}</div>}
            {profileErr && <div className="alert alert-danger p-2 small d-flex align-items-center gap-2"><AlertCircle size={16} />{profileErr}</div>}

            <form onSubmit={handleProfileSubmit}>
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Full Name</label>
                  <div className="input-group">
                    <span className="input-group-text bg-secondary border-secondary text-light"><User size={16} /></span>
                    <input
                      type="text"
                      className="form-control bg-secondary text-light border-secondary"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="col-md-6">
                  <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Email Address</label>
                  <div className="input-group">
                    <span className="input-group-text bg-secondary border-secondary text-light"><Mail size={16} /></span>
                    <input
                      type="email"
                      className="form-control bg-secondary text-light border-secondary"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>
                </div>
              </div>

              <div className="mt-4 text-end">
                <button type="submit" className="btn btn-primary d-inline-flex align-items-center gap-2 px-4" disabled={profileLoading}>
                  <Save size={16} />
                  {profileLoading ? 'Saving...' : 'Update Profile'}
                </button>
              </div>
            </form>
          </div>

          {/* Change Password Form */}
          <div className="card bg-dark border-secondary p-4 text-light">
            <h5 className="fw-bold mb-3 d-flex align-items-center gap-2">
              <Key className="text-primary" size={20} />
              Change Password
            </h5>

            {pwdMsg && <div className="alert alert-success p-2 small d-flex align-items-center gap-2"><CheckCircle size={16} />{pwdMsg}</div>}
            {pwdErr && <div className="alert alert-danger p-2 small d-flex align-items-center gap-2"><AlertCircle size={16} />{pwdErr}</div>}

            <form onSubmit={handlePasswordSubmit}>
              <div className="row g-3">
                <div className="col-md-4">
                  <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Current Password</label>
                  <input
                    type="password"
                    className="form-control bg-secondary text-light border-secondary"
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    required
                  />
                </div>

                <div className="col-md-4">
                  <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>New Password</label>
                  <input
                    type="password"
                    className="form-control bg-secondary text-light border-secondary"
                    placeholder="Min 8 chars"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                  />
                </div>

                <div className="col-md-4">
                  <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Confirm New Password</label>
                  <input
                    type="password"
                    className="form-control bg-secondary text-light border-secondary"
                    placeholder="Re-enter new password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="mt-4 text-end">
                <button type="submit" className="btn btn-warning d-inline-flex align-items-center gap-2 px-4 text-dark fw-bold" disabled={pwdLoading}>
                  <Key size={16} />
                  {pwdLoading ? 'Updating Password...' : 'Change Password'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
