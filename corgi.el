(defvar corgi-org-file-path
    (shell-command-to-string "python -c \"from config import org_file; print org_file\""))

(defvar corgi-org-file (file-name-nondirectory corgi-org-file-path))

(defun sync-to-taskpaper ()
  "Sync org file to taskpaper file for mobile access"
  (when (file-equal-p buffer-file-name corgi-org-file-path)
    (shell-command "~/corgi.sh taskpapersync")))

(add-hook 'after-save-hook #'sync-to-taskpaper)

(defun sync-with-corgi ()
  "Sync org file with to_sync.txt from corgi capture and mobile capture"
  (when (window-system nil)
    (message (shell-command-to-string "./corgi.sh orgsync"))))

(defun es/sync-corgi-tasks ()
  "Close org file if open and write new tasks to it"
  (let ((taskfile (get-buffer corgi-org-file)))
    (when taskfile
      (switch-to-buffer taskfile)
      (save-buffer)
      (kill-buffer taskfile))
    (message (shell-command-to-string "./corgi.sh orgsync"))))

(defun es/org-agenda ()
  (interactive)
  (es/sync-corgi-tasks)
  (org-agenda)
)

;; (add-hook 'org-finalize-agenda-hook #'es/sync-corgi-tasks)

(add-hook 'after-init-hook #'sync-with-corgi)
