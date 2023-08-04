import * as fs from "node:fs/promises";
import * as dotenv from "dotenv";
import { ServiceAuthorizationClient } from "@itwin/service-authorization";
import { RealityConversionService } from "reality-capture";
import { RCJobSettings } from "reality-capture/lib/rcs/Utils";

dotenv.config({
  path: "../.env"
});

const iTwinId = process.env.IMJS_PROJECT_ID ?? "";
const clientId = process.env.IMJS_CLIENT_ID ?? "";
const clientSecret = process.env.IMJS_SECRET ?? "";
const authority = process.env.IMJS_ISSUER_URL ?? "";
const env = process.env.IMJS_ENV ?? "";

const scope = Array.from(RealityConversionService.getScopes()).join(" ");

const authClient = new ServiceAuthorizationClient({
  clientId,
  clientSecret,
  scope,
  authority
});

const INPUTS_FILE = "../data/inputs.json";
const FAILED_INPUTS_FILE = "../data/failed_inputs.json";
const JOBS_INFO_FILE = "../data/jobs_info.json";

async function cancelJob(jobId: string) {
  const rcsClient = new RealityConversionService(authClient);
  await rcsClient.cancelJob(jobId);
  console.log("Cancelled job: ", jobId);
}

async function runJob(inputType: string, inputId: string) {
  const rcsClient = new RealityConversionService(authClient);
  const jobSettings = new RCJobSettings();
  (jobSettings.inputs as any)[inputType] = [inputId];
  jobSettings.outputs.opc = true;
  const jobID = await rcsClient.createJob(
    jobSettings,
    `${inputType.toUpperCase()}-to-OPC`,
    iTwinId
  );
  await rcsClient.submitJob(jobID);
  console.log("Submitted job:", jobID);
  return jobID;
}

async function runRcsBenchmark() {
  const jobsInfo: any = JSON.parse(
    (await fs.readFile(JOBS_INFO_FILE)).toString()
  );
  const failedInputs: any = {};
  const inputs = JSON.parse((await fs.readFile(INPUTS_FILE)).toString());
  const inputTypes = Object.keys(inputs);

  if (!jobsInfo.jobIds) jobsInfo.jobIds = [];

  for (let inputType of inputTypes) {
    if (!jobsInfo[inputType]) jobsInfo[inputType] = [];
    console.log(`${inputType.toUpperCase()} jobs`);

    for (let inputId of inputs[inputType]) {
      try {
        const jobId = await runJob(inputType, inputId);
        jobsInfo[inputType].push({ jobId, inputId });
        jobsInfo.jobIds.push(jobId);
      } catch (error: any) {
        console.log("Error occured for input:", inputId);
        console.log(error);
        if (!failedInputs[inputType]) failedInputs[inputType] = [inputId];
        else failedInputs[inputType].push(inputId);
      }
    }

  }

  await fs.writeFile(JOBS_INFO_FILE, JSON.stringify(jobsInfo));
  await fs.writeFile(FAILED_INPUTS_FILE, JSON.stringify(failedInputs));
}

runRcsBenchmark();
// cancelJob("41f0e13a-273c-4bfd-914c-14868a910738");
// runJob("laz", "759faeb9-0c15-4cd5-9f46-d2228943fa85");
