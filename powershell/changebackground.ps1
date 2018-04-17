Try {
	$url = "http://i.imgur.com/KM3fIrb.jpg"
	$filePath = "$env:USERPROFILE\test.jpg"
	$wc = New-Object System.Net.WebClient
	$wc.DownloadFile($url, $filePath)

	Function WaitForDownload($File)
	{
		  while(!(Test-Path $File)) 
		  {
				Start-Sleep -s 5;
		  }

	}
	Function Set-WallPaper($Value)
	{
		Set-ItemProperty -path 'HKCU:\Control Panel\Desktop\' -name "Wallpaper" -value "$filePath"
		Set-ItemProperty -path 'HKCU:\Control Panel\Desktop\' -name "WallpaperStyle" -value 0
		rundll32.exe user32.dll, UpdatePerUserSystemParameters
	}
	WaitForDownload($filePath)
	Start-Sleep -s 20
	Set-WallPaper
}
Catch
{
	$ErrorMessage = $_.Exception.Message
    $FailedItem = $_.Exception.ItemName
	Write-Host $ErrorMessage
	Write-Host
	Write-Host "Press any key to continue ..."

	$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}