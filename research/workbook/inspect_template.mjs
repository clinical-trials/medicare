import fs from 'node:fs/promises';
import {Workbook, SpreadsheetFile, FileBlob} from '@oai/artifact-tool';
const path='/Users/lgm/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-analytics-dashboard/assets/reference.xlsx';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:2500})).ndjson);
console.log(wb.help('range.hyperlink',{include:'index,notes,examples',maxChars:3000}).ndjson);
