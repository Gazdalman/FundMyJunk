import { useDispatch, useSelector } from "react-redux";
import { useModal } from "../../context/Modal";
import { deleteProject, setRequestedProject } from "../../store/userProjects";
import "./DeleteModal.css"
import { deleteReward } from "../../store/project";
import { useHistory } from "react-router-dom";

const DeleteModal = ({ method, project, reward, type }) => {
  const dispatch = useDispatch();
  const history = useHistory();
  const { closeModal } = useModal();
  const user = useSelector(state => state.session.user)

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (type == "project") {
      e.preventDefault()
      await dispatch(deleteProject(project.id))
      history.push("/")
    } else {
      e.preventDefault()
      e.stopPropagation()

      const res = await dispatch(deleteReward(reward.id));
      if (res === 'ok')
        dispatch(setRequestedProject(reward.projectId));
    }
    closeModal()
  }

  return (
    <>
      <h1 id="delete-form-title">Confirm Delete</h1>
      <form className="delete-form" onSubmit={e => handleSubmit(e)}>
        <p style={{ width: 200 }} id="delete-text">{type === "reward" ? "Are you sure you want to delete this reward?" : "Are you sure you want to remove this project?"}</p>
        <button style={{ width: 200, height: 45 }} type="submit" id="confirm-delete">Yes ({type === "reward" ? "Delete Reward" : "Delete Project"})</button>
        <button type="button" style={{ marginBottom: "35px", width: 200, height: 45 }} onClick={() => closeModal()} id="cancel-delete">No ({type === "reward" ? "Keep Reward" : "Keep Project"})</button>
      </form>
    </>
  )
}

export default DeleteModal
