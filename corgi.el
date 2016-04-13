(defvar corgi-org-file-path
    (shell-command-to-string "python -c \"from config import org_file; print org_file\"")
    "Path to org file retrieved from python config file")

(defvar corgi-org-file (file-name-nondirectory corgi-org-file-path)
    "Name of org file")

(defun corgi-sync-to-taskpaper ()
  "Sync org file to taskpaper file for mobile access"
  (when (file-equal-p buffer-file-name corgi-org-file-path)
    (shell-command "./runcorgi.sh taskpapersync")))

(defun corgi-sync-to-org-command ()
    (message (shell-command-to-string "./runcorgi.sh orgsync")))

(defun corgi-sync-to-org-initially ()
  "Sync org file with to_sync.txt from corgi capture and mobile capture"
  (when (window-system nil)
    (corgi-sync-to-org-command)))

(defun corgi-sync-to-org ()
  "Close org file if open and write new tasks to it"
  (let ((taskfile (get-buffer corgi-org-file)))
    (when taskfile
      (switch-to-buffer taskfile)
      (save-buffer)
      (kill-buffer taskfile))
    (corgi-sync-to-org-command)))

(defun corgi-org-agenda ()
  (interactive)
  (corgi-sync-to-org)
  (org-agenda)
)

(add-hook 'after-save-hook #'corgi-sync-to-taskpaper)
(add-hook 'after-init-hook #'corgi-sync-to-org-initially)
