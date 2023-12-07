import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams, useHistory } from "react-router-dom";
import { setRequestedProject } from "../../store/userProjects";

const ProjectPage = () => {
  const history = useHistory();
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false)
  const { projectId } = useParams();
  const user = useSelector(state => state.session.user);
  const [project, setProject] = useState("")
  useEffect(() => {
    const loadProject = async () => {
      const gotProject = await dispatch(setRequestedProject(projectId))
      setProject(gotProject)
    }
    loadProject()
    setIsLoaded(true)
  }, [dispatch]);
  return (
    <h1>{}</h1>
  )
}

export default ProjectPage
