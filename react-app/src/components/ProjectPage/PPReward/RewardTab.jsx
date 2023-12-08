import OpenModalButton from "../../OpenModalButton";
import PPRewardTab from "../PPForms/PPReward";
import "./RewardTab.css"
import { useState } from "react";
import { useDispatch } from "react-redux";
import { setRequestedProject } from "../../../store/userProjects";
import { useHistory } from "react-router-dom"
import { deleteReward } from "../../../store/project";

const RewardTab = ({ rewards, user, projectOwner, projId }) => {
  const dispatch = useDispatch()
  const history = useHistory()
  const [showForm, setShowForm] = useState(false)

  const changeDate = (date) => {
    const selectedDate = new Date(date);

    const month = selectedDate.toLocaleString('default', { month: 'long' });
    const year = selectedDate.getFullYear();
    return `${month.slice(0, 3)} ${year}`
  }

  const loginRedirect = (e) => {
    e.preventDefault()
    return history.push("/login")
  }

  const noFundingYet = (e) => {
    e.preventDefault()

    window.alert("You can't spend your money yet. Which is good because this is a terrible idea...")
  }

  const openRewardForm = (e) => {
    e.preventDefault()
    setShowForm(true)
  }

  const deleteAReward = async (e, id) => {
    e.preventDefault()
    e.stopPropagation()

    const res = await dispatch(deleteReward(id));
    if (res === 'ok')
      dispatch(setRequestedProject(projId));

  }

  return rewards ? (
    !showForm ? (<div>
      {rewards.map(reward => (
        <div key={reward.id} id="pp-reward-card">
          <div id="pp-reward-card-image">
            <img id="pp-rcd-image" src={reward.image} alt={reward.title} />
          </div>
          <div id="pp-reward-card-details">
            <div id="pp-rcd-upper">
              <h3 id="pp-rcd-title">{reward.title}</h3>
              <h3 id="pp-rcd-amount">${reward.amount}</h3>
            </div>
            <div id="pp-rcd-mid">
              {reward.physicalItems &&
                <div id="mid-shipping">
                  <p id="ms-header">Shipping</p>
                  <p id="ms-body">{reward.shipping}</p>
                </div>
              }
              <div id="mid-delivery">
                <p id="md-header">Estimated Delivery</p>
                <p id="md-body">{changeDate(reward.deliveryDate)}</p>
              </div>
              {!reward.unlimited &&
                <div id="mid-quantity">
                  <p id="mq-header">Limited Quantity</p>
                  <p id="mq-body">{reward.quantity} left</p>
                </div>
              }
            </div>
            <div id="pp-rcd-lower">
              {reward.description ? <p id="pp-rcd-desc">{reward.description}</p> : <p>No Description</p>}
              {reward.items.map(item => (
                <div key={item.id} id="pp-rcd-item">
                  <div id="pp-item-details">
                    <p>{item.title}</p>
                    <p>Quantity: {item.quantity}</p>
                  </div>
                  {item.image && <img id="pp-item-image" src={item.image} />}
                </div>
              ))}
              {user ? (user != projectOwner ?
                <button id="pp-rcd-pledge-button" onClick={noFundingYet}>Pledge ${reward.amount}</button> : <button id="pp-rcd-delete-button" onClick={(e) => deleteAReward(e, reward.id)}>Delete Reward</button>) :
                <button id="no-user-login-pledge" onClick={e => loginRedirect(e)}>Login to Pledge</button>
              }
            </div>
          </div>

        </div>

      ))}
      {(user && user == projectOwner) ?
        <button onClick={openRewardForm} id="add-reward-button">Add Reward</button> : null}
    </div>
    )
      : <PPRewardTab
        projectId={projId}
        setShowForm={setShowForm}
      />) : ""
}

export default RewardTab
