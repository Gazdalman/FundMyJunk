import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux";
import { deleteProject, getUserProjects } from "../../../store/userProjects";
import { useHistory } from "react-router-dom";
import "../ProfilePage.css"
import OpenModalButton from "../../OpenModalButton";
import DeleteModal from "../../utilities/deleteModal";
import ProjectTab from "./ProjectTab";
import EarnedRewards from "./EarnedRewards";
import LikedProjects from "./LikedProjects";

const ProfilePage = () => {
  const dispatch = useDispatch()
  const history = useHistory()
  const currUser = useSelector(state => state.session.user);
  const projects = useSelector(state => state.userProjects);
  const projArr = Object.values(projects);
  const [isLoaded, setIsLoaded] = useState(false);
  const [tab, setTab] = useState("projects")

  useEffect(() => {
    const getProjects = async () => {
      await dispatch(getUserProjects(currUser.id))
      setIsLoaded(true)
    }
    getProjects()
  }, [dispatch])
  return isLoaded ? (
    <div id="ppp-div">
      <div id="ppp-header">
        <div id="ppp-header-left">
          <img id="ppp-profile-pic" src={currUser.profile.profilePic ? currUser.profile.profilePic : "https://fmjbucket.s3.us-east-2.amazonaws.com/79dd0d67ffc34097b913489257727a00.gif"} alt="profile-pic" />
          <i className="fas fa-camera"></i>
        </div>
        <div id="ppp-header-mid">
          <h3>{currUser.displayName}</h3>
          <h2>{currUser.profile.private ? currUser.username : `${currUser.profile.firstName} ${currUser.profile.lastName}`}</h2>

        </div>
      </div>
      <div id="ppp-tabs">
        <h3 id="ppp-projects-tab" className="link" onClick={() => setTab("projects")}>Projects</h3>
        <h3 id="ppp-rewards-tab" className="link" onClick={() => setTab("pledges")}>Pledges</h3>
        <h3 id="ppp-backed-tab" className="link" onClick={() => setTab("liked")}>Liked</h3>
      </div>
      {tab == "projects" && <ProjectTab projArr={projArr} />}
      {tab == "pledges" && <EarnedRewards earnedRewards={currUser.backed} userId={currUser.id} />}
      {tab == "liked" && <LikedProjects userId={currUser.id} likedProjects={Object.values(currUser.liked)} />}
    </div>
  ) : <h1 className="loading-message">We Loadin...</h1>
}

export default ProfilePage
