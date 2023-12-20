import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import { signUp } from "../../store/session";
import "./SignupForm.css";

function SignupFormModal() {
	const dispatch = useDispatch();
	const [focused, setFocused] = useState("");
	const [email, setEmail] = useState("");
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [firstName, setFirstName] = useState("");
	const [lastName, setLastName] = useState("");
	const [displayName, setDisplayName] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const [errors, setErrors] = useState([]);
	const { closeModal } = useModal();

	const isValidEmail = (email) => {
		// Regular expression pattern for basic email validation
		const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

		// Test the email against the pattern
		return emailPattern.test(email);
	}

	const handleFocus = (field, e) => {
		e.preventDefault()
		setFocused(field);
	};

	const handleBlur = () => {
    setFocused("false");
  };

	const handleSubmit = async (e) => {
		e.preventDefault();
		if (password === confirmPassword) {
			const data = await dispatch(signUp(username, firstName, email, password));
			if (data) {
				setErrors(data);
			} else {
				closeModal();
			}
		} else {
			setErrors([
				"Confirm Password field must be the same as the Password field",
			]);
		}
	};

	return (
		<div id="sign-up-modal-form">
			<h1>Sign Up</h1>
			<form onSubmit={handleSubmit}>
				<ul>
					{((!email || !isValidEmail(email)) && focused == "email") && <li>Email must be... well.. an email.</li>}
				</ul>
				<div className={`sum-email-field floating-input ${focused == "email" ? 'focused' : ''}`}>
					<label className={`sef-label input-label ${focused == "email" || email ? 'label-focus' : ''}`}>
						Email*
					</label>
					<input
						type="email"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						onFocus={e => handleFocus("email", e)}
						onBlur={handleBlur}
						className="sef-input input-field"
						required
					/>
				</div>
				<div className={`sum-username-field floating-input ${focused == "username" ? 'focused' : ''}`}>
					<label className={`suf-label input-label ${focused == "username" || username ? 'label-focus' : ''}`}>
						Username*
					</label>
					<input
						type="text"
						value={username}
						onChange={(e) => setUsername(e.target.value)}
						onFocus={e => handleFocus("username", e)}
						onBlur={handleBlur}
						className="suf-input input-field"
						required
					/>
				</div>
				<div className={`sum-first-field floating-input ${focused == "firstName" ? 'focused' : ''}`}>
					<label className={`sff-label input-label ${focused == "firstName" || firstName ? 'label-focus' : ''}`}>
						First Name*
					</label>
					<input
						type="text"
						value={firstName}
						onChange={(e) => setFirstName(e.target.value)}
						onFocus={e => handleFocus("firstName", e)}
						onBlur={handleBlur}
						className="sff-input input-field"
						required
					/>
				</div>
				<div className={`sum-password-field floating-input ${focused == "password" ? 'focused' : ''}`}>
					<label className={`spf-label input-label ${focused == "password" || password ? 'label-focus' : ''}`}>
						Password
					</label>
					<input
						type="password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						onFocus={e => handleFocus("password", e)}
						onBlur={handleBlur}
						className="spf-input input-field"
						required
					/>
				</div>
				<div className={`sum-confirm-field floating-input ${focused == "confirmPassword" ? 'focused' : ''}`}>
					<label className={`scf-label input-label ${focused == "confirmPassword" || confirmPassword ? 'label-focus' : ''}`}>
						Confirm Password
					</label>
					<input
						type="password"
						value={confirmPassword}
						onChange={(e) => setConfirmPassword(e.target.value)}
						onFocus={e => handleFocus("confirmPassword", e)}
						onBlur={handleBlur}
						className="scf-input input-field"
						required
					/>
				</div>
				<button type="submit">Sign Up</button>
			</form>
		</div>
	);
}

export default SignupFormModal;
