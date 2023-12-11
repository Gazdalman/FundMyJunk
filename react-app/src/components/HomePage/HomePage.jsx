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

  const addCommas = (number) => {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  useEffect(() => {
    dispatch(getAllProjects())
    setIsLoaded(true)
  }, [dispatch])

  return isLoaded && projArr.length ? (
    <div id="home-page">
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
              <div id="hp-mid">
                <div id="hp-earned">
                  <span id="hp-earned-upper">${addCommas(project.earned.toFixed(2))}</span>
                  <span id="hp-earned-lower">pledged</span>
                </div>
                <div id="hp-percent-earned">
                  <span id="hp-percent-earned-upper">{(+project.earned / +project.goal).toFixed(2) * 100}%</span>
                  <span id="hp-percent-earned-lower">earned</span>
                </div>
                <div id="hp-days-left">
                  <span id="hp-days-left-upper">{daysLeft(project.endDate) + 1}</span>
                  <span id="hp-days-left-lower">days left</span>
                </div>
              </div>
              <div id="hp-bottom">
                <span id="hp-subcategory">{project.mainSub}</span>
                <span id="hp-location">{project.location}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  ) : null
}

export default HomePage
