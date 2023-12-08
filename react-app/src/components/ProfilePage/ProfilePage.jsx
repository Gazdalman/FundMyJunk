import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux";
import { deleteProject, getUserProjects } from "../../store/userProjects";
import { useHistory } from "react-router-dom";

const ProfilePage = () => {
  const dispatch = useDispatch()
  const history = useHistory()
  const currUser = useSelector(state => state.session.user);
  const projects = useSelector(state => state.userProjects);
  const projArr = Object.values(projects);
  const [isLoaded, setIsLoaded] = useState(false);

  const editClick = (e, projectId) => {
    e.preventDefault()
    return history.push(`/projects/${projectId}/edit`)
  }

  const deleteClick = async (e, projectId) => {
    e.preventDefault()
    setIsLoaded(false)
    await dispatch(deleteProject(projectId))
    await dispatch(getUserProjects(currUser.id))
    setIsLoaded(true)

  }

  const goTo = (link) => {
    return history.push(link)
  }

  useEffect(() => {
    const getProjects = async () => {
      await dispatch(getUserProjects(currUser.id))
      setIsLoaded(true)
    }
    getProjects()
  }, [dispatch])
  return isLoaded ? (
    <>
      <h1>{currUser.id}</h1>
      {projArr.map(project => (
        <div key={project.id}>
          <h3 className="link" onClick={() => goTo(`/projects/${project.id}`)} >{project.title}</h3>
          <button onClick={e => editClick(e, project.id)}>Edit This</button>
          <button onClick={e => deleteClick(e, project.id)}>Delete This</button>
        </div>
      
      ))}
    </>
  ) : <h1 className="loading-message">We Loadin...</h1>
}

export default ProfilePage
