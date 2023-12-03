import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { getAllProjects } from "../../store/project";

const HomePage = () => {
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

  useEffect(() => {
    dispatch(getAllProjects())
    setIsLoaded(true)
  }, [dispatch])

  return isLoaded && projArr.length ? (
    <>
      <h1>Top Earners</h1>
      {projArr.map(project => (
        <div key={project.id} id="home-project-card">
          <a href={`/projects/${project.id}`}>
            <img src={project.image} id="hp-img" />
          </a>
          <a href={`/projects/${project.id}`}>
            <h3 id="hp-title">{project.title}</h3>
          </a>
          <p id="hp-subtitle">{project.subtitle}</p>
          <span id="hp-author">
            by <a href={`/users/${project.userId}`}>
              {project.user}
            </a>
          </span>
          <progress value={project.earned} max={project.goal}></progress>
          <span id="hp-earned">${project.earned.toFixed(2)} pledged</span>
          <span id="hp-percent-earned">{(+project.earned / +project.goal).toFixed(2) * 100}% earned</span>
          <span id="hp-days-left">{daysLeft(project.endDate) + 1} days left</span>
          <div id="hp-bottom">
            <span id="hp-subcategory">{project.mainSub}</span>
            <span id="hp-location">{project.location}</span>
          </div>
        </div>
      ))}
    </>
  ) : null
}

export default HomePage
