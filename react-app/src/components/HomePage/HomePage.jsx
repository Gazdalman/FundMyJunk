import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { getAllProjects } from "../../store/project";
import "./HomePage.css"
import { useHistory } from "react-router-dom";

const HomePage = () => {
  const history = useHistory()
  const projects = useSelector(state => state.projects)
  const projArr = Object.values(projects)
  const [isLoaded, setIsLoaded] = useState(false);
  // const [progress, setProgress] = useState(0);
  const dispatch = useDispatch()

  const daysLeft = (date) => {
    const today = new Date();
    const end = new Date(date)
    const difference = end - today;

    return Math.floor(difference / (1000 * 60 * 60 * 24))
  }

  const goTo = (link) => {
    return history.push(link)
  }

  useEffect(() => {
    dispatch(getAllProjects())
    setIsLoaded(true)
  }, [dispatch])

  return isLoaded && projArr.length ? (
    <>
      <h1 id="home-page-title">Top Earners</h1>
      <div id="home-page-cards">
        {projArr.map(project => (
          <div key={project.id} className="home-project-card">
            <img className="link" id="hp-card-img" onClick={() => goTo(`/projects/${project.id}`)} src={project.image} />
            <div id="hp-card-details">
              <h3 className="link" onClick={() => goTo(`/projects/${project.id}`)} id="hp-title">{project.title}</h3>
              <p id="hp-subtitle">{project.subtitle}</p>
              <span>by
                <span className="link" onClick={() => goTo(`/users/${project.userId}`)} id="hp-author"> {project.user}
                </span>
              </span>
              <progress id="hp-progress" value={project.earned} max={project.goal}></progress>
              <span id="hp-earned">${project.earned.toFixed(2)} pledged</span>
              <span id="hp-percent-earned">{(+project.earned / +project.goal).toFixed(2) * 100}% earned</span>
              <span id="hp-days-left">{daysLeft(project.endDate) + 1} days left</span>
              <div id="hp-bottom">
                <span id="hp-subcategory">{project.mainSub}</span>
                <span id="hp-location">{project.location}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  ) : null
}

export default HomePage
