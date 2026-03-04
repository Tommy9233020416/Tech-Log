
(cl:in-package :asdf)

(defsystem "ros_learning-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :actionlib_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "LandingAction" :depends-on ("_package_LandingAction"))
    (:file "_package_LandingAction" :depends-on ("_package"))
    (:file "LandingActionFeedback" :depends-on ("_package_LandingActionFeedback"))
    (:file "_package_LandingActionFeedback" :depends-on ("_package"))
    (:file "LandingActionGoal" :depends-on ("_package_LandingActionGoal"))
    (:file "_package_LandingActionGoal" :depends-on ("_package"))
    (:file "LandingActionResult" :depends-on ("_package_LandingActionResult"))
    (:file "_package_LandingActionResult" :depends-on ("_package"))
    (:file "LandingFeedback" :depends-on ("_package_LandingFeedback"))
    (:file "_package_LandingFeedback" :depends-on ("_package"))
    (:file "LandingGoal" :depends-on ("_package_LandingGoal"))
    (:file "_package_LandingGoal" :depends-on ("_package"))
    (:file "LandingResult" :depends-on ("_package_LandingResult"))
    (:file "_package_LandingResult" :depends-on ("_package"))
  ))