param([string]$Doc, [string]$Pdf)
$word = New-Object -ComObject Word.Application
try {
  $word.Visible = $false
  $word.DisplayAlerts = 0
  $d = $word.Documents.Open($Doc, $false, $false, $false)
  try {
    foreach ($toc in $d.TablesOfContents) { $toc.Update() }
    $d.Save()
    $d.ExportAsFixedFormat($Pdf, 17)
    Write-Output ("{0} pages" -f $d.ComputeStatistics(2))
  } finally { $d.Close([ref]0) }
} finally {
  $word.Quit([ref]0)
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
}
