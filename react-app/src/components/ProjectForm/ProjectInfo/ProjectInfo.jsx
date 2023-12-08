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
  type
}) => {
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
      setEndDate("")
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
      <div className={`proj-title-field floating-input ${focused == "title" ? 'focused' : ''}`}>
        <label className={`ptf-label input-label ${focused == "title" || title ? 'label-focus' : ''}`}>
          Title
        </label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onFocus={e => handleFocus("title", e)}
          onBlur={handleBlur}
          className="ptf-input input-field"
        />
      </div>
      <div className={`proj-subtitle-field floating-input ${focused == "subtitle" ? 'focused' : ''}`}>
        <label className={`psf-label input-label ${focused == "subtitle" || subtitle ? 'label-focus' : ''}`}>
          Subtitle
        </label>
        <input
          type="text"
          value={subtitle}
          onChange={(e) => setSubtitle(e.target.value)}
          onFocus={e => handleFocus("subtitle", e)}
          onBlur={handleBlur}
          className="psf-input input-field"
        />
      </div>
      <div className={`proj-goal-field floating-input ${focused == "goal" ? 'focused' : ''}`}>
        <label className={`pgf-label input-label ${focused == "goal" || goal ? 'label-focus' : ''}`}>
          Goal
        </label>
        <input
          type="number"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          onFocus={e => handleFocus("goal", e)}
          onBlur={handleBlur}
          className="pgf-input input-field"
        />
      </div>
      <PhotoField
        image={image}
        setImage={setImage}
        setImageURL={setImageURL}
        imageURL={imageURL}
      />
      <VideoField
        setVideo={setVideo}
        video={video}
        videoURL={videoURL}
        setVideoURL={setVideoURL}
      />
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
      <div id="dates-div">
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
      </div>
    </div>
  )
}

export default ProjectInfo
