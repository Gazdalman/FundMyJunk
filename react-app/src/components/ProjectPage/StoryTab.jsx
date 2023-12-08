import EditStoryForm from "./PPForms/EditStory";
import OpenModalButton from "../OpenModalButton";
import PPStoryForm from "./PPForms/PPStoryForm";
const StoryTab = ({ story, projectUser, id, user }) => {
  return story ? (
    <>
      <h2>Story</h2>
      <span>{story.text}</span>
      <span>{story.risks_challenges}</span>
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
      <h1>Story</h1>
      <div id="pp-add-story">
        <span>No Story on this project</span>
        {(user && projectUser == user.id) &&
          <OpenModalButton
            modalClasses={["pp-add-product-btn"]}
            modalComponent={<PPStoryForm projectId={id} />}
          />}
      </div>
    </>
  )
}

export default StoryTab
