import { useState } from "react"
import { useSelector } from "react-redux";

const ProfilePage = () => {
  const currUser = useSelector(state => state.session.user);

  return (
    <h1>{currUser.id}</h1>
  )
}

export default ProfilePage
