import { useState } from "react"
import MainCategory from "./MainCategory";

const ProjectForm = ({ type, project }) => {
  const [tab, setTab] = useState("basics")
  const [title, setTitle] = useState(type == "edit" ? project.title : "");
  const [subtitle, setSubtitle] = useState(type == "edit" ? project.subtitle : "");
  const [location, setLocation] = useState(type == "edit" ? project.location : "");
  const [projType, setProjType] = useState(type == "edit" ? project.type : "");
  const [image, setImage] = useState(type == "edit" ? project.image : "");
  const [video, setVideo] = useState(type == "edit" ? project.video : "");
  const [goal, setGoal] = useState(type == "edit" ? project.goal : "");
  const [launchDate, setLaunchDate] = useState(type == "edit" ? project.launchDate : "");
  const [endDate, setEndDate] = useState(type == "edit" ? project.endDate : "");
  const [mainCategory, setMainCategory] = useState(type == "edit" ? project.mainCategory : "");
  const [mainSubcat, setMainSubcat] = useState(type == "edit" ? project.mainSub : "");
  const [secondCat, setSecondCat] = useState(type == "edit" ? project.secondCat : "");
  const [secondSubcat, setSecondSubcat] = useState(type == "edit" ? project.secondSub : "");
  const [launched, setLaunched] = useState(type == "edit" ? project.launched : false);

  return (
    <div id="project-form-container">
      <div id="form-tabs">
        <h3 id="category-location-tab">Basics</h3>
      </div>
      {tab == "basics" && <MainCategory
        mainCategory={mainCategory}
        mainSubcat={mainSubcat}
        setMainCategory={setMainCategory}
        setMainSubcat={setMainSubcat}
      />}
    </div>

  )
}

export default ProjectForm
