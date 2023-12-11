import EditStoryForm from "./PPForms/EditStory";
import OpenModalButton from "../OpenModalButton";
import PPStoryForm from "./PPForms/PPStoryForm";
const StoryTab = ({ story, projectUser, id, user }) => {
  return story ? (
    <>
      <h2>Story</h2>
      <h3>About This Project</h3>
      <span style={{overflowWrap: "break-word"}}>{story.text}</span>
      <h3>Potential Risks</h3>
      <span style={{overflowWrap: "break-word"}}>{story.risks_challenges}</span>
      {(story && user && projectUser == user.id ) && <div id="buttons-links">
        <OpenModalButton
          modalComponent={<EditStoryForm story={story} projectId={id} />}
          modalClasses={["edit-story-button"]}
          buttonText={"Edit Story"}
          onClick={e => e.preventDefault()}
        />
      </div>
      }
    </>

  ) : (
    <>
      <h2>Story</h2>
      <div id="pp-add-story">
        <span>No Story on this project</span>
        {(user && projectUser == user.id) &&
          <OpenModalButton
            modalClasses={["pp-add-story-btn"]}
            modalComponent={<PPStoryForm projectId={id} />}
            buttonText={"Add Story"}
          />}
      </div>
    </>
  )
}

export default StoryTab
