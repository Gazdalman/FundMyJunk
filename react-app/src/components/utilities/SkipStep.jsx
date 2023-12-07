import { useModal } from "../../context/Modal"

const SkipStep = ({ skipStep }) => {
  const { closeModal } = useModal()

  const handleSkip = (e) => {
    e.preventDefault()
    skipStep()
    closeModal()
  }

  const handleCancel = (e) => {
    e.preventDefault()
    closeModal()
  }

  return (
    <div id="skip-step">
      <h2>Skip This Step?</h2>
      <div id="ss-buttons">
        <button onClick={handleSkip}>Yes</button>
        <button onClick={handleCancel}>No</button>
      </div>
    </div>
  )
}

export default SkipStep
