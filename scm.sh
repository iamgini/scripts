#!/bin/bash

# Function to extract the main Git URL and open it in the browser
open_git_url() {
    local git_path=$1

    # Check if the directory is a Git repository
    if git -C "$git_path" rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        # Get the Git remote URL
        git_url=$(git -C "$git_path" config --get remote.origin.url)

        # Handle SSH/SSH-like URLs (e.g., ssh://git@gitlab.consulting.abc.com:2222/bau/ansible-onboarding.git)
        if [[ $git_url =~ ^ssh://git@ ]] || [[ $git_url =~ ^git@ ]]; then
            # Remove the ssh:// if it exists
            git_url=${git_url#ssh://}

            # Split into protocol, host, and path
            protocol="https://"
            host_and_port=${git_url%%/*}  # Everything before the first '/'
            repo_path=${git_url#*/}       # Everything after the first '/'

            # Remove the port if it exists (anything after ':')
            host=${host_and_port%%:*}

            # Reconstruct the URL
            git_url="$protocol$host/$repo_path"
        else
            # Handle regular HTTPS URLs
            # Remove any 'git@' if present and keep everything after '@'
            git_url=${git_url/git@/}
        fi

        # Remove any potential ".git" suffix from the URL
        git_url=$(echo "$git_url" | sed -e 's/\.git$//')

        # Open the repository's main URL in the default web browser (Chrome)
        xdg-open "$git_url"
    else
        echo "Not a Git repository: $git_path"
        exit 1
    fi
}

# If an argument is provided, use it as the path; otherwise, use the current directory
path=${1:-$(pwd)}

open_git_url "$path"
