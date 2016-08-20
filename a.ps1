git filter-branch --env-filter \
		'if [ $GIT_COMMIT = 27906f368b599b813fce824bf20e95d58bb50ec8 ]
		 then
			 export GIT_AUTHOR_DATE="2016-08-15T11:48:36"
	         export GIT_COMMITTER_DATE="2016-08-15T11:48:36"
		 fi'