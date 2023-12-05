import React, { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { Route, Switch } from "react-router-dom";
import SignupFormPage from "./components/SignupFormPage";
import LoginFormPage from "./components/LoginFormPage";
import { authenticate } from "./store/session";
import Navigation from "./components/Navigation";
import HomePage from "./components/HomePage/HomePage";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import ProfilePage from "./components/ProfilePage/ProfilePage";
import ProjectForm from "./components/ProjectForm";
import UserProfilePage from "./components/ProfilePage/UserProfilePage";
import EditProject from "./components/EditProject/EditProject";

function App() {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false);
  useEffect(() => {
    dispatch(authenticate()).then(() => setIsLoaded(true));
  }, [dispatch]);

  return (
    <>
      <Navigation isLoaded={isLoaded} />
      {isLoaded && (
        <Switch>
          <Route exact path="/">
            <HomePage />
          </Route>
          <Route path="/login" >
            <LoginFormPage />
          </Route>
          <Route path="/signup">
            <SignupFormPage />
          </Route>
          <ProtectedRoute path="/profile">
            <ProfilePage />
          </ProtectedRoute>
          <Route path="/users/:id">
            <UserProfilePage />
          </Route>
          <ProtectedRoute path="/new_project">
            <ProjectForm />
          </ProtectedRoute>
          <ProtectedRoute path="/projects/:projectId/edit">
            <EditProject />
          </ProtectedRoute>
        </Switch>
      )}
    </>
  );
}

export default App;
