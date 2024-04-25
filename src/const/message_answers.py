FIRST_START_ANS = "⚙️First launch\n👨‍💻Administrator rights have been granted"

NOT_PERMISSION_ANS = "You not have permission!"

MAIN_MENU_ANS = "🏠Main Menu"
MESSAGE_NOT_REG_ANS = "Choose an option⬇️"

ADDED_ANS = "➕Added"
DELETED_ANS = "➖Removed"

# ===================================== Cameras ===================================================
LOAD_STATUSES_ANS = "Load cameras ..."  # If press cameras in main menu
CAM_STATUSES_LIST_ANS = "🔵Status   ─  Name\n"

CAMERA_ONLINE_ANS = "🟢Online  "
CAMERA_OFFLINE_ANS = "🔴Offline "

ENTER_CAMERA_NAME_ANS = "Enter camera name:"
ENTER_CAMERA_NAME_ERR_ANS = "Camera with that name already exists!"

ADD_CAMERA_RTSP_ANS = "Enter RTSP/s address:"
ADD_CAMERA_RTSP_NOT_ANS = 'RTSP/s address startswith: "rtsp://", "rtsps://"'
ADD_CAMERA_RTSP_ERR_ANS = "Camera with that RTSP already exists!"
ADD_CAMERA_PING_ERR_ANS = "Camera not available!"
CAMERA_ADDED_ANS = "✅Camera <b>{name}</b> added"

DEL_CAMERA_NAME_ANS = "Select the camera to delete: "
DEL_CAMERA_DONE_ANS = "🗑Camera <b>{name}</b> deleted"

PHOTO_LOAD_ANS = "Loading photo ..."
PHOTO_CAMERA_SELECT_ANS = "Select the camera to get photo: "
# =================================================================================================

# ===================================== Records ===================================================
RECORDS_ACTIVE_ANS = "🟢Active "
RECORDS_ERROR_ANS = "🔴Error  "
ACTIVE_RECORDS_ANS = "Active records\n🔵Status   ─  Name  ─  Time left\n "
ACTIVE_RECORDS_NONE_ANS = "No active records"

RECORDS_SELECT_CAMERA_ANS = "Select camera: "
RECORDS_SELECT_CAMERA_REC_ANS = "The camera is already recording.\nStop recording to start another!"
RECORDS_SELECT_CAMERA_ERR_ANS = "Camera not available!"
RECORDS_ENTER_DURATION_ANS = "Enter duration of record in minutes: "
RECORDS_RUN_ACCEPTED_ANS = "✅Camera <b>{name}</b> recording for <b>{duration}</b> minutes accepted"

RECORDS_STOP_ACCEPTED_ANS = "⏹Camera <b>{name}</b> recording stopped"
# ================================================================================================


# ===================================== Schedule ==================================================
DAYS_STRING = {1: "Mo", 2: "Tu", 3: "We", 4: "Th", 5: "Fr", 6: "Sa", 7: "Su"}
SCHEDULE_FORMAT_LIST_ANS = "{id:^3}|{s:^7}|{d:^8}| {c}  ─  {days}\n"
SCHEDULE_LIST_ANS = SCHEDULE_FORMAT_LIST_ANS.format(id="id", s="Start", d="Duration", c="Cameras", days="Days")
SCHEDULE_EMPTY_ANS = "Schedule is Empty!"

SCHEDULE_ENTER_TIME_ANS = "Enter start time"
SCHEDULE_ENTER_TIME_ERR_ANS = "Not a valid time.\nPlease send time in format HH:MM"

SCHEDULE_ENTER_DURATION_ANS = "Enter duration in minutes"
SCHEDULE_ENTER_DURATION_ERR_ANS = "Not a valid duration.\nPlease send 1-1440 minutes"

SCHEDULE_SELECT_CAMERAS_IKB_ANS = "Select cameras to recording"
SCHEDULE_SELECT_CAMERAS_RKB_ANS = "And press confirm"
SCHEDULE_SELECT_CAMERAS_EMPTY_ANS = "You haven't selected any cameras"
SCHEDULE_SELECT_CAMERAS_ERR_ANS = "Please select cameras to recording and press confirm"

SCHEDULE_SELECT_DAYS_ANS = "Select days to record"
SCHEDULE_SELECT_DAYS_EMPTY_ANS = "You haven't selected any days"
SCHEDULE_SELECT_DATS_ERR_ANS = "Please select days to recording and press confirm"

SCHEDULE_ADD_ERR = "Error adding schedule, error: {name}"
SCHEDULE_CONFIRM_ANS = "✅Schedule added"

SCHEDULE_DELETE_ANS = "Send id schedule"
SCHEDULE_DELETE_ERR_ANS = "There is no schedule with this id"
SCHEDULE_DELETED_ANS = "🗑Deleted schedule"
