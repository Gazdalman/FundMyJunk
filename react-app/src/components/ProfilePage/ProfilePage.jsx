import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux";
import { getUserProjects } from "../../store/userProjects";
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
          <h3>{project.title}</h3>
          <button onClick={e => editClick(e, project.id)}>Edit This</button>
        </div>

      ))}
    </>
  ) : null
}

export default ProfilePage
