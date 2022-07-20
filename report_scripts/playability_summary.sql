SELECT DISTINCT tbltitles.name,  tbltitles.gameID, tbltitles.releasedate, tblbenchmarks.benchmarkID, tblPlatforms.bucketID, tbltitles.have_thumbnail, 
	 
    tblbenchmarks.num_screenshots, tblbenchmarks.num_configs
	FROM tblbenchmarks 
		JOIN tblTitles ON tblbenchmarks.gameID = tblTitles.gameID
        JOIN tblPlatforms ON tblbenchmarks.platformID = tblPlatforms.platformID
		ORDER BY gameID ASC, bucketID ASC, description

