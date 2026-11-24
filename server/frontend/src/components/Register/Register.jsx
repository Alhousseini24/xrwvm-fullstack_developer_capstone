import React, { useState } from 'react';

const Register = ({ onRegister }) => {
  const [form, setForm] = useState({
    userName: '',
    password: '',
    firstName: '',
    lastName: '',
    email: '',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('/djangoapp/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (data.status === 'Authenticated') {
        onRegister(data);
      } else {
        setError(data.error || 'Erreur lors de l\'inscription');
      }
    } catch (err) {
      setError('Erreur réseau');
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '500px' }}>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Username</label>
          <input type="text" name="userName" className="form-control"
                 value={form.userName} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">Password</label>
          <input type="password" name="password" className="form-control"
                 value={form.password} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">First Name</label>
          <input type="text" name="firstName" className="form-control"
                 value={form.firstName} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">Last Name</label>
          <input type="text" name="lastName" className="form-control"
                 value={form.lastName} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">Email</label>
          <input type="email" name="email" className="form-control"
                 value={form.email} onChange={handleChange} required />
        </div>
        {error && <div className="alert alert-danger">{error}</div>}
        <button type="submit" className="btn btn-primary">Register</button>
      </form>
    </div>
  );
};

export default Register;