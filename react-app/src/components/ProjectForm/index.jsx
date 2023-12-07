import { useEffect, useState } from "react"
import Basics from "./Basics/Basics";
import ProjectInfo from "./ProjectInfo/ProjectInfo";
import { useDispatch } from "react-redux";
import { createProject, editProject } from "../../store/project";
import { useHistory } from "react-router-dom";

const ProjectForm = ({ type, project }) => {
  const history = useHistory()
  const dispatch = useDispatch();
  const id = type == "edit" ? project.id : null
  const [flip, setFlip] = useState("on")
  const [disabled, setDisabled] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [tab, setTab] = useState("basics");
  const [title, setTitle] = useState(type == "edit" ? project.title : "");
  const [subtitle, setSubtitle] = useState(type == "edit" ? project.subtitle : "");
  const [location, setLocation] = useState(type == "edit" ? project.location : "");
  const [projType, setProjType] = useState(type == "edit" ? project.type : "");
  const [image, setImage] = useState("");
  const [video, setVideo] = useState("");
  const [imageURL, setImageURL] = useState(type == "edit" ? project.image : "");
  const [videoURL, setVideoURL] = useState(type == "edit" ? project.video : "");
  const [goal, setGoal] = useState(type == "edit" ? project.goal : "");
  const [launchDate, setLaunchDate] = useState(type == "edit" ? project.launchDate : "");
  const [endDate, setEndDate] = useState(type == "edit" ? project.endDate : "");
  const [mainCategory, setMainCategory] = useState(type == "edit" ? project.mainCategory : "");
  const [mainSubcat, setMainSubcat] = useState(type == "edit" ? project.mainSub : "");
  const [secondCat, setSecondCat] = useState(type == "edit" ? project.secondCat : "");
  const [secondSubcat, setSecondSubcat] = useState(type == "edit" ? project.secondSub : "");
  const [launched, setLaunched] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault()

    const projectData = new FormData()

    projectData.append("title", title)
    projectData.append("subtitle", subtitle)
    projectData.append("location", location)
    projectData.append("type", projType)
    if (type == 'edit') {
      if (image) {
        projectData.append("image", image)
      }

      if (video) {
        projectData.append("video", video)
      }
    } else {
      projectData.append("image", image)
      if (video) {
        projectData.append("video", video)
      }
    }

    projectData.append("goal", goal)
    const launch = new Date(launchDate)
    projectData.append("launchDate", launch.toISOString().split("T")[0])
    const end = new Date(endDate)
    projectData.append("endDate", end.toISOString().split("T")[0])
    projectData.append("mainCategory", mainCategory)
    projectData.append("mainSubcat", mainSubcat)
    projectData.append("secondCat", secondCat)
    projectData.append("secondSubcat", secondSubcat)

    setUploading(true)
    if (type != "edit") {
      const res = await dispatch(createProject(projectData))
      setUploading(false)
      if (!res.errors) return history.push(`/projects/${res.id}/add_story`)
    } else {
      const res = await dispatch(editProject(projectData, id))
      setUploading(false)
      if (!res.errors) return history.push(`/projects/${res.id}`)
    }
  }

  useEffect(() => {
    if (subtitle.length >= 10
      && projType
      // && (type != "edit" && image)
      && goal >= 1
      && mainCategory
      && mainSubcat
      && (title.length >= 3)
      && launchDate
      && endDate
    ) {
      setDisabled(false)
    } else {
      setDisabled(true)
    }
    setFlip(flip == "on" ? "off" : "on")
  }, [mainCategory, subtitle, title, mainSubcat, launchDate, goal, projType, image, location])

  useEffect(() => {
    if (type == "edit") {
      const today = new Date().toISOString().split("T")[0];
      if (today >= project.launchDate) setLaunched(true)
    }
  }, [])

  return !uploading ? (
    <div id="project-form-container">
      <div id="form-tabs">
        <span onClick={() => setTab("basics")} id="basics-tab">Basics</span>
        <span onClick={() => setTab("project-info")} id="project-info-tab">Project Details</span>
      </div>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        {tab == "basics" && <Basics
          mainCategory={mainCategory}
          mainSubcat={mainSubcat}
          setMainCategory={setMainCategory}
          setMainSubcat={setMainSubcat}
          secondCat={secondCat}
          setSecondCat={setSecondCat}
          secondSubcat={secondSubcat}
          setSecondSubcat={setSecondSubcat}
          location={location}
          setLocation={setLocation}
        />}
        {tab == "project-info" && <ProjectInfo
          endDate={endDate}
          launchDate={launchDate}
          image={image}
          video={video}
          imageURL={imageURL}
          videoURL={videoURL}
          projType={projType}
          goal={goal}
          title={title}
          subtitle={subtitle}
          setTitle={setTitle}
          setSubtitle={setSubtitle}
          setGoal={setGoal}
          setProjType={setProjType}
          setVideo={setVideo}
          setVideoURL={setVideoURL}
          setImage={setImage}
          setImageURL={setImageURL}
          setLaunchDate={setLaunchDate}
          setEndDate={setEndDate}
        />}
        <button disabled={disabled}> Confirm Project</button>
      </form>
      <div></div>
    </div>

  ) : <h1 className="loading-message">We Loadin...</h1>
}

export default ProjectForm
