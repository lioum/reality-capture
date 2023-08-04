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
  const inputs = JSON.parse((await fs.readFile(INPUTS_FILE)).toString());
  const inputTypes = Object.keys(inputs);

  if (!jobsInfo.jobIds) jobsInfo.jobIds = [];

  for (let inputType of inputTypes) {
    if (!jobsInfo[inputType]) jobsInfo[inputType] = [];
    console.log(`${inputType.toUpperCase()} jobs`);

    try {
      for (let inputId of inputs[inputType]) {
        const jobId = await runJob(inputType, inputId);
        jobsInfo[inputType].push({ jobId, inputId });
        jobsInfo.jobIds.push(jobId);
      }
    } catch (error: any) {
      console.log(JSON.stringify(error));
    }

  }

  await fs.writeFile(JOBS_INFO_FILE, JSON.stringify(jobsInfo));
}

runRcsBenchmark();
// cancelJob("7676245f-eb2a-4ded-8fae-1a695e8f2cac");
