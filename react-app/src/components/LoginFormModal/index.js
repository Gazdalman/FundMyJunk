import React, { useState } from "react";
import { login } from "../../store/session";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import "./LoginForm.css";
import OpenModalButton from "../OpenModalButton";
import SignupFormModal from "../SignupFormModal";

function LoginFormModal() {
  const dispatch = useDispatch();
  const [cred, setCred] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState([]);
  const { closeModal } = useModal();

  const loginDemo = (e) => {
    e.preventDefault()
    dispatch(login('demoNoodle', 'password'))
    closeModal()
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await dispatch(login(cred, password));
    if (data) {
      setErrors(data);
    } else {
        closeModal()
    }
  };

  return (
    <div id="login-form-modal">
      <h1>Log In</h1>
      <form onSubmit={handleSubmit}>
        <ul>
          {errors.map((error, idx) => (
            <li key={idx}>{error}</li>
          ))}
        </ul>
        <label>
          Credential
          <input
            type="text"
            value={cred}
            onChange={(e) => setCred(e.target.value)}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <button type="submit">Log In</button>
        <OpenModalButton
        modalClasses={["logInRedirect"]}
        modalComponent={<SignupFormModal />}
        buttonText="... or Sign Up Here"
      />
        <button onClick={loginDemo}>Demo User</button>
      </form>
    </div>
  );
}

export default LoginFormModal;
