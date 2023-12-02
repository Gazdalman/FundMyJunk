import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { getAllProjects } from "../../store/project";

const HomePage = () => {
  const projects = useSelector(state => state.projects)
  const [isLoaded, setIsLoaded] = useState(false);
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(getAllProjects())
    setIsLoaded(true)
  }, [dispatch])

  return isLoaded && projects ? (
    <>
    <h1>Hello</h1>
    {Object.values(projects).map((project) => (
      <div key={project.id}>
        <h3>{project.title}</h3>
      </div>
    ))}
    </>
  ) : null
}

export default HomePage
