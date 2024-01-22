import { useState } from "react";
import { useDispatch } from "react-redux";
import { createPledge } from "../../store/pledge";
import { useModal } from "../../context/Modal";
import { setRequestedProject } from "../../store/userProjects";

const PledgeForm = ({ projId }) => {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const [amount, setAmount] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await dispatch(createPledge({"amount": amount}, projId));
    await dispatch(setRequestedProject(projId));
    closeModal();
  }

  return (
    <div id="pledge-div">
    <h1>Pledge</h1>
    <form onSubmit={handleSubmit}>
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
      />
      <button type="submit">Pledge</button>
    </form>
    </div>
  )
}

export default PledgeForm
