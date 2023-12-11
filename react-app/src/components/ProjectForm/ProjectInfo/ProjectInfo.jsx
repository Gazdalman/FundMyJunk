import { useEffect, useState } from "react";
import PhotoField from "../../utilities/PhotoField";
import VideoField from "../../utilities/VideoField";
import moment from 'moment';

const ProjectInfo = ({
  endDate,
  launchDate,
  image,
  video,
  projType,
  goal,
  title,
  subtitle,
  setTitle,
  setSubtitle,
  setGoal,
  setProjType,
  setVideo,
  setImage,
  setLaunchDate,
  setEndDate,
  setImageURL,
  setVideoURL,
  imageURL,
  videoURL,
  type,
  setTab,
  errs
}) => {
  const originalDate = endDate
  const [focused, setFocused] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const today = new Date().toISOString().split("T")[0];

  const launchChange = (e) => {
    setEndDate("")
    setLaunchDate(e.target.value)
  }

  const launchLimit = () => {
    let lastDay = new Date()
    lastDay.setDate(lastDay.getDate() + 30)
    return lastDay.toISOString().split('T')[0];
  }

  const tabChange = (e) => {
    e.preventDefault()
    setTab("basics")
  }

  const endLimit = () => {
    let endDay = new Date(launchDate)
    endDay.setDate(endDay.getDate() + 60)
    return endDay.toISOString().split('T')[0]
  }

  const handleFocus = (field, e) => {
    e.preventDefault()
    setFocused(field);
  };

  const handleBlur = () => {
    setFocused("false");
  };

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };

  useEffect(() => {
    if (selectedOption == "30-days") {
      let endDay = new Date(launchDate)
      endDay.setDate(endDay.getDate() + 30)
      setEndDate(endDay.toISOString().split('T')[0])
    } else if (selectedOption == "60-days") {
      let endDay = new Date(launchDate)
      endDay.setDate(endDay.getDate() + 60)
      setEndDate(endDay.toISOString().split("T")[0])
    } else if (selectedOption == "specific") {
      if (type != 'edit') {
        setEndDate("")
      }
    }
  }, [selectedOption])

  useEffect(() => {
    if (launchDate) {
      let launch = new Date(launchDate)
      setLaunchDate(launch.toISOString().split("T")[0])
    }
    if (endDate) {
      let end = new Date(endDate)
      setEndDate(end.toISOString().split("T")[0])
    }
  }, [])

  return (
    <div id="proj-info-form">
      <div id="project-title-area">
        <div id="project-title-info">
          <h2>Title</h2>
          <div id="project-title-description">
            <p>Name your project something interesting so that you can grab the short attention spans of the public and convince them to spend their hard earned money on your awful idea!</p>
            <p style={{ "color": "red" }}>{errs.title ? errs.title : "(Make it at least 3 characters good sir)"}</p>
          </div>
        </div>
        <div className={`proj-title-field floating-input ${focused == "title" ? 'focused' : ''}`}>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onFocus={e => handleFocus("title", e)}
            onBlur={handleBlur}
            className="ptf-input input-field"
          />
        </div>
      </div>
      <div id="project-subtitle-area">
        <div id="project-subtitle-info">
          <h2>Subtitle</h2>
          <div id="project-title-description">
            <p>This should explain your project a bit. Just! A! Bit!</p>
            <p style={{ "color": "red" }}>(May be squished or stretched beyond belief)</p>
          </div>
        </div>
        <div className={`proj-subtitle-field floating-input ${focused == "subtitle" ? 'focused' : ''}`}>
          <input
            type="text"
            value={subtitle}
            onChange={(e) => setSubtitle(e.target.value)}
            onFocus={e => handleFocus("subtitle", e)}
            onBlur={handleBlur}
            className="psf-input input-field"
          />
        </div>
      </div>
      <div id="project-goal-area">
        <div id="project-gaol-info">
          <h2>Goal</h2>
          <div id="project-goal-description">
            <p>This, my friend, is the beautiful number of monies the people will pay us and by extension, YOU! <span style={{ "font-size": "10px" }}>maybe</span></p>
          </div>
        </div>
        <div className={`proj-goal-field floating-input ${focused == "goal" ? 'focused' : ''}`}>
          <input
            type="number"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            onFocus={e => handleFocus("goal", e)}
            onBlur={handleBlur}
            className="pgf-input input-field"
          />
        </div>
      </div>
      <div id="project-image-field">
        <div id="project-image-info">
          <h2>Project Image</h2>
          <div id="project-image-description">
            <p>Give the people a pretty picture to gawk at!</p>
            <p style={{ "color": "red" }}>(10 to 100 characters)</p>
          </div>
        </div>
        <div id="project-dnd-box">
          <PhotoField
            image={image}
            setImage={setImage}
            setImageURL={setImageURL}
            imageURL={imageURL}
          />
        </div>
      </div>
      <div id="video-field">
        <h2>Project Video (Optional)</h2>
        <div id="project-dnd-box">
          <VideoField
            setVideo={setVideo}
            video={video}
            videoURL={videoURL}
            setVideoURL={setVideoURL}
          />
        </div>
      </div>
      <div id="type-select">
        <label id="type-label">
          Project Type
        </label>
        <select onChange={e => setProjType(e.target.value)} value={projType} className="input-field" id="type-selector">
          <option value="" disabled>--Select--</option>
          <option value="business">Business</option>
          <option value="non-profit">Non-Profit</option>
          <option value="personal">Personal</option>
        </select>
      </div>
      {(type != "edit" || today >= new Date(launchDate)) && <div id="dates-div">
        <input
          value={launchDate}
          type="date"
          min={type != "edit" ? today : launchDate}
          max={launchLimit()}
          onChange={launchChange}
          className="input-field"
        />
        <div id="end-date-selector">
          <div id="ed-radio">
            <label>
              <input
                disabled={!launchDate}
                type="radio"
                value="30-days"
                checked={selectedOption === "30-days"}
                onChange={handleOptionChange}
              />
              End 30 days after you launch
            </label>
            <label>
              <input
                disabled={!launchDate}
                type="radio"
                value="60-days"
                checked={selectedOption === "60-days"}
                onChange={handleOptionChange}

              />
              End 60 days after you launch
            </label>
            <label>
              <input
                disabled={!launchDate}
                type="radio"
                value="specific"
                checked={selectedOption === "specific"}
                onChange={handleOptionChange}
              />
              Select a specific date
            </label>
          </div>
          <input
            disabled={!launchDate || selectedOption != "specific"}
            value={endDate}
            type="date"
            min={launchDate}
            max={launchDate ? endLimit() : ""}
            onChange={(e) => setEndDate(e.target.value)}
            className="input-field"
          />
        </div>
      </div>}
      <div id="back-button-container">
        <button id="back-basics-button" onClick={tabChange}>Back To Basics</button>
      </div>
    </div>
  )
}

export default ProjectInfo
