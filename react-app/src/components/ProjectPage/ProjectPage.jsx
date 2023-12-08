import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams, useHistory } from "react-router-dom";
import { deleteProject, setRequestedProject } from "../../store/userProjects";
import StoryTab from "./StoryTab";
import RewardTab from "./PPReward/RewardTab";
import "./ProjectPage.css"
import DeleteModal from "../utilities/deleteModal";
import OpenModalButton from "../OpenModalButton";

const ProjectPage = () => {
  const history = useHistory();
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false)
  const [tab, setTab] = useState("rewards")
  const { projectId } = useParams();
  const project = useSelector(state => state.userProjects)
  const user = useSelector(state => state.session.user);

  const setHours = () => {
    const launch = new Date(project.launchDate)
    const end = new Date(project.endDate)
    const difference = end - launch

    // if (Math.floor(difference / (1000 * 60 * 60 * 24)) > 2)
    //   return Math.floor(difference / (1000 * 60 * 60 * 24))

    return Math.floor(difference / (1000 * 60 * 60))
  }

  const editClick = (e, projectId) => {
    e.preventDefault()
    return history.push(`/projects/${projectId}/edit`)
  }

  const deleteClick = async (e, projectId) => {
    e.preventDefault()
    setIsLoaded(false)
    await dispatch(deleteProject(projectId))
    await dispatch(setRequestedProject(user.id))
    setIsLoaded(true)
  }

  const setDays = () => {
    const launch = new Date(project.launchDate)
    const end = new Date(project.endDate)
    const difference = end - launch
    return Math.ceil(difference / (1000 * 60 * 60 * 24))
  }

  const blink = () => {
    return window.location.reload(true)
  }

  useEffect(() => {
    const loadProject = async () => {
      const gotProject = await dispatch(setRequestedProject(projectId))
      if (gotProject.not_found) {
        return history.replace("/not_found")
      }
    }
    loadProject()
    setIsLoaded(true)
  }, [dispatch]);

  return (
    <div id="project-page-container">
      <div id="pp-header">
        <h1>{project.title}</h1>
        <h2>{project.subtitle}</h2>
      </div>
      <div id="pp-project-details">
        <div id="pp-image-container">
          {!project.video ? <img id="pp-image" src={project.image} alt={`image for project ${project.id}`} /> : <video id="pp-video" src={project.video} controls controlsList="nodownload"></video>}
        </div>
        <div id="pp-details-container">
          <progress value={project.earned} max={project.goal} />
          <span>${project.earned}<span>earned toward goal of ${project.goal}</span></span>
          <span>{project.launched ? (setHours() <= 48 ? setHours() : setDays()) : "Not"}<span>{project.launched ? (setHours() <= 48 ? "Hours Left" : "Days Left") : "Launched"}</span></span>
        </div>
      </div>
      <div id="pp-tabs">
        <span onClick={() => setTab("story")} id="story-tab">Story</span>
        <span onClick={() => setTab("rewards")} id="rewards-tab">Rewards</span>
      </div>
      {tab == "story" && <div id="pp-story-tab">
        <StoryTab
          story={project.story}
          projectUser={project.userId}
          id={project.id}
          user={user}
        />
      </div>}
      {tab == "rewards" && <div id="pp-rewards-tab">
        <RewardTab projId={project.id} rewards={project.rewards} user={user ? user.id : 0} projectOwner={project.userId} />
      </div>}
      {user.id == project.userId && <div id="user-project-buttons">
        <button onClick={e => editClick(e, project.id)}>Edit Project</button>
        <OpenModalButton
        modalClasses={["delete-button"]}
        modalComponent={<DeleteModal project={project} type={"project"}/>}
        buttonText={"Delete Project"}
         />
      </div>}
    </div>
  )
}

export default ProjectPage
