(defvar corgi-org-file-path
    (shell-command-to-string "python -c \"from config import org_file; print org_file\"")
    "Path to org file retrieved from python config file")

(defvar corgi-org-file (file-name-nondirectory corgi-org-file-path)
    "Name of org file")

(defvar corgi-working-directory
  (if load-file-name
      (file-name-directory load-file-name)
      default-directory))

(defun corgi-sync-to-taskpaper ()
    "Sync org file to taskpaper file for mobile access"
    (shell-command (concat corgi-working-directory "runcorgi.sh taskpapersync")))

(defun corgi-sync-to-org-command ()
    (message (shell-command-to-string (concat corgi-working-directory "runcorgi.sh orgsync"))))

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

(advice-add 'org-agenda-quit :after #'corgi-sync-to-taskpaper)

(add-hook 'after-init-hook #'corgi-sync-to-org-initially)
