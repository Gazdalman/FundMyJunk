import React from "react";
import { NavLink } from "react-router-dom";
import { useSelector } from "react-redux";
import ProfileButton from "./ProfileButton";
import "./Navigation.css";

function Navigation({ isLoaded }) {
	const sessionUser = useSelector(state => state.session.user);

	const search = async (e) => {
		e.preventDefault();
		const search = document.getElementById("search-input").value;
		const res = await fetch(`/api/search/${search}`);
		const data = await res.json();
		if (res.ok) {
			console.log(data);
		}
	}

	return (
		<nav>
			<ul id="nav-bar">
				<li id="home">
					<NavLink className="eh" exact to="/">
						<img id="home-logo" src="https://fmjbucket.s3.us-east-2.amazonaws.com/79dd0d67ffc34097b913489257727a00.gif" />
						{/* <img id="home-logo-text" src="https://fmjbucket.s3.us-east-2.amazonaws.com/d90590a565054290b8236174db116a13.gif"/>
						 */}
						<span id="home-logo-text">FundMyJunk</span>
					</NavLink>
				</li>
				<li id="search-bar">
					<input id="search-input" type="text" placeholder="Search" />
					<button id="search-button" type="submit">
						<i className="fas fa-search"></i>
					</button>
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
