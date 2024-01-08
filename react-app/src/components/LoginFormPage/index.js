import React, { useState } from "react";
import { login } from "../../store/session";
import { useDispatch, useSelector } from "react-redux";
import { Redirect, useHistory } from "react-router-dom";
import './LoginForm.css';

function LoginFormPage() {
  const history = useHistory()
  const dispatch = useDispatch();
  const sessionUser = useSelector((state) => state.session.user);
  const [cred, setCred] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState([]);
  const [focused, setFocused] = useState("");

  if (sessionUser) return <Redirect to="/" />;

  const handleFocus = (field, e) => {
    e.preventDefault()
    setFocused(field);
  };

  const handleBlur = () => {
    setFocused("false");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await dispatch(login(cred, password));
    if (data) {
      setErrors(data);
    }
    return history.goBack()
  };

  const loginDemo = (e) => {
    e.preventDefault()
    dispatch(login('demoNoodle', 'password'))
    return history.goBack()
  }

  return (
    <>
      <h1>Log In</h1>
      <form onSubmit={handleSubmit}>
        <ul>
          {errors.map((error, idx) => (
            <li key={idx}>{error}</li>
          ))}
        </ul>
        <div className={`lm-cred-field floating-input ${focused == "cred" ? 'focused' : ''}`}>
          <label className={`lcf-label input-label ${focused == "cred" || cred ? 'label-focus' : ''}`}>
            Credential
          </label>
          <input
            type="text"
            value={cred}
            onChange={(e) => setCred(e.target.value)}
            onFocus={e => handleFocus("cred", e)}
            onBlur={handleBlur}
            className="lcf-input input-field"
            required
          />
        </div>
        <div className={`lm-email-field floating-input ${focused == "password" ? 'focused' : ''}`}>
          <label className={`lef-label input-label ${focused == "password" || password ? 'label-focus' : ''}`}>
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onFocus={e => handleFocus("password", e)}
            onBlur={handleBlur}
            className="lpf-input input-field"
            required
          />
        </div>
        <button className="account-button" type="submit">Log In</button>
        <button className="account-button" onClick={loginDemo}>Demo User</button>
      </form>
    </>
  );
}

export default LoginFormPage;
