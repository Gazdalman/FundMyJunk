import { useEffect, useState } from "react"
import { setRequestedProject } from "../../store/userProjects";
import { useParams, useHistory } from "react-router-dom";
import { useDispatch } from "react-redux";
import { createStory } from "../../store/project";
import OpenModalButton from "../OpenModalButton";
import SkipStep from "../utilities/SkipStep";

const StoryForm = () => {
  const history = useHistory();
  const dispatch = useDispatch();
  const [selectedAI, setSelectedAI] = useState("");
  const [isLoaded, setIsLoaded] = useState(false)
  const [focused, setFocused] = useState("");
  const [project, setProject] = useState("");
  const { projectId } = useParams();
  const [disabled, setDisabled] = useState(true);
  const [ai, setAi] = useState("");
  const [storyText, setStoryText] = useState("")
  const [risksChallenges, setRisksChallenges] = useState("")

  const skipStep = () => {
    return history.replace(`/projects/${projectId}/add_reward`)
  }

  const handleStorySubmit = async (e) => {
    e.preventDefault()
    const newStory = new FormData()
    newStory.append("ai", ai)
    newStory.append("storyText", storyText)
    newStory.append("risksChallenges", risksChallenges)
    const res = await dispatch(createStory(newStory, projectId))
    if (res == "ok") {
      return history.replace(`/projects/${projectId}/add_reward`)
    }
  }

  const handleAIChange = (e) => {
    setAi(e.target.value)
    setSelectedAI(e.target.value);
  };

  const handleFocus = (field, e) => {
    e.preventDefault()
    setFocused(field);
  };

  const handleBlur = () => {
    setFocused("false");
  };

  useEffect(() => {
    if (ai != "" &&
      storyText && storyText.length > 3 &&
      risksChallenges && risksChallenges.length > 3
    ) {
      setDisabled(false)
    }
  }, [ai, storyText, risksChallenges])

  useEffect(() => {
    const loadProject = async () => {
      const gotProject = await dispatch(setRequestedProject(projectId))
      if (gotProject.story) return history.push(`/projects/${projectId}`)
      setProject(gotProject)
    }
    loadProject()
    setIsLoaded(true)
  }, [dispatch]);
  return (
    <div id="story-form-container">
      <form onSubmit={handleStorySubmit} encType="multipart/form-data">
        <h1>Add a Story</h1>
        <div id="ai-input-field">
          <label className="ai-option">
            <input
              type="radio"
              value="true"
              checked={selectedAI === "true"}
              onChange={handleAIChange}
            />
            Yes, I am using AI for my project
          </label>
          <label className="ai-option">
            <input
              type="radio"
              value="false"
              checked={selectedAI === "false"}
              onChange={handleAIChange}
            />
            No, I am not using AI for my project
          </label>
          <div className={`story-text-field floating-input ${focused == "story" ? 'focused' : ''}`}>
            <label className={`stf-label input-label ${focused == "story" || storyText ? 'label-focus' : ''}`}>
              Story Text
            </label>
            <textarea
              value={storyText}
              onChange={(e) => setStoryText(e.target.value)}
              onFocus={e => handleFocus("story", e)}
              onBlur={handleBlur}
              className="stf-input input-field"
            />
          </div>
          <div className={`story-risk-field floating-input ${focused == "risk" ? 'focused' : ''}`}>
            <label className={`srf-label input-label ${focused == "risk" || risksChallenges ? 'label-focus' : ''}`}>
              Risks and Challenges
            </label>
            <textarea
              value={risksChallenges}
              onChange={(e) => setRisksChallenges(e.target.value)}
              onFocus={e => handleFocus("risk", e)}
              onBlur={handleBlur}
              className="srf-input input-field"
            />
          </div>
        </div>
        <button disabled={disabled}>Save Story</button>
      </form>
      <OpenModalButton
          modalComponent={<SkipStep skipStep={skipStep}/>}
          buttonText={"Skip Step"}
          modalClasses={["skip-step-button"]}
          />
    </div>
  )
}

export default StoryForm
