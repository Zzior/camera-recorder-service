# ===================================== __main__ ==================================================
TASK_ERROR_LOG = "Error task cancel Exception: {e}"

# ===================================== Admin_router ==============================================
ADMIN_CAMERAS_IKB_LOG = "Error bot.edit_message_reply_markup in admin_menu -> cameras: {e}"
ADMIN_DAYS_IKB_LOG = "Error bot.edit_message_reply_markup in admin_menu -> days: {e}"
ADMIN_SCHEDULE_ADD_LOG = "Error adding schedule: {e}"

# ===================================== RecordManager =============================================
CAMERA_NOT_FOUND_LOG = "Camera '{name}' not found in cameras"
CAMERA_NOW_RECORD_LOG = "Camera '{name}' is already being recorded"
CAMERA_NOT_PING_LOG = "Camera {name} is not available"

RECORD_RUN_LOG = "Starting recording for {name}"
END_RECORD_LOG = "Finished recording for {name}"

STOP_RECORD_LOG = "Stopping recording for {name}"
KILL_RECORD_LOG = "Kill recording for {name}"

ERROR_RECORD_LOG = "Error recording for {name} return code: {rc}\nstdout:{sout}\nstderr:{serr}"
FORCED_STOP_LOG = "Camera {camera} forced shutdown!"
RESUME_RECORD_LOG = "Camera {name} recording resumed"
REACHED_RECORD_LOG = "Camera {name} to resume recording, minimum recording time has been reached"
# =================================================================================================

# ===================================== NotifyManager =============================================
SEND_NOTIFY_ERR_LOG = "Error while notifying\nevent: {name}\ntg_id: {id}\nException: {e}"
# =================================================================================================
