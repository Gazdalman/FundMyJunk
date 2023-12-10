import { useDispatch, useSelector } from "react-redux";
import { useModal } from "../../context/Modal";
import { deleteProject, setRequestedProject } from "../../store/userProjects";
import "./DeleteModal.css"
import { deleteItem, deleteReward } from "../../store/project";
import { useHistory } from "react-router-dom";

const DeleteModal = ({ method, project, reward, item, projId, type }) => {
  const dispatch = useDispatch();
  const history = useHistory();
  const { closeModal } = useModal();
  const user = useSelector(state => state.session.user)

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (type == "project") {
      await dispatch(deleteProject(project.id))
      history.push("/")
    } else if (type == "reward") {
      const res = await dispatch(deleteReward(reward.id));
      if (res === "ok")
        dispatch(setRequestedProject(reward.projectId));
    } else {
      const res = await dispatch(deleteItem(item.id))
      if (res == "ok")
      dispatch(setRequestedProject(projId))
    }
    closeModal()
  }

  return (
    <>
      <h1 id="delete-form-title">Confirm Delete</h1>
        <p
          style={{ width: 200 }}
          id="delete-text">
          {type === "reward" ?
            "Are you sure you want to delete this reward?" :
            (type === "project" ?
              "Are you sure you want to remove this project?" :
              "Are you sure you want to remove this item from this reward?"
            )}</p>
        <button
        onClick={e => handleSubmit(e)}
          style={{ width: 200, height: 45 }}
          type="submit" id="confirm-delete">Yes ({
            type === "reward" ?
              "Delete Reward" :
              (type === "project" ?
                "Delete Project" :
                "Delete Item")})</button>
        <button
          type="button"
          style={{ marginBottom: "35px", width: 200, height: 45 }}
          onClick={() => closeModal()} id="cancel-delete">No ({
            type === "reward" ? "Keep Reward" :
              (type == "project" ? "Keep Project" :
                "Keep Item")})</button>
    </>
  )
}

export default DeleteModal
