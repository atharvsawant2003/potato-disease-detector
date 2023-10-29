import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import { useCookies } from 'react-cookie';
import './Login.css'

function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [message, setMessage] = useState('');
  const [cookies, setCookie, removeCookie] = useCookies(['ajs_anonymous_id']);

  useEffect(() => {
    if (cookies.ajs_anonymous_id) {
      navigate('/home');
    }
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/login', formData);
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Login failed. Please check your credentials.');
    }
  };
 
  if (message === "Your are Sucessfully login") {
    navigate('/home');
  }

  return (
    <div className="form-box">
      <form className="form" onSubmit={handleSubmit}>
        <span className="title">Login</span>
        <div className="form-container">
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="input"
              placeholder="Username"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="input"
              placeholder="Password"
            />
          </div>
        </div>
        <button type="submit" className="submit-button">
          Login
        </button>
      </form>
      <p className="message">{message}</p>
      <p>
        Need to create an account? <Link to="/register">Sign Up</Link>
      </p>
    </div>
  );
}

export default Login;
