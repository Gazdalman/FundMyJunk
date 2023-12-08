import React from "react";
import { NavLink } from "react-router-dom";
import { useSelector } from "react-redux";
import ProfileButton from "./ProfileButton";
import "./Navigation.css";

function Navigation({ isLoaded }) {
	const sessionUser = useSelector(state => state.session.user);

	return (
		<nav>
			<ul id="nav-bar">
				<li id="home">
					<NavLink className="eh" exact to="/">
						<img id="home-logo" src="https://fmjbucket.s3.us-east-2.amazonaws.com/79dd0d67ffc34097b913489257727a00.gif"/>
						{/* <img id="home-logo-text" src="https://fmjbucket.s3.us-east-2.amazonaws.com/d90590a565054290b8236174db116a13.gif"/>
						 */}
						 <span id="home-logo-text">FundMyJunk</span>
						</NavLink>
				</li>
				{isLoaded && (
					<li id="profile-button">
						<ProfileButton user={sessionUser} />
					</li>
				)}
			</ul>
</nav>

	);
}

export default Navigation;
