/*---------------------------------------------------------------------------------------------
* Copyright (c) Bentley Systems, Incorporated. All rights reserved.
* See LICENSE.md in the project root for license terms and full copyright notice.
*--------------------------------------------------------------------------------------------*/

import { Button, Checkbox, LabeledInput, Alert, ProgressRadial, Dialog } from "@itwin/itwinui-react";
import React, { useEffect } from "react";
import "./ContextCapture.css";
import { CCJobInformation, JobTracking } from "./Models";

import SvgPlay from "@itwin/itwinui-icons-react/cjs/icons/Play";

interface CccsProps {
    accessToken: string,
    jobs: CCJobInformation[]
    setJobs: React.Dispatch<React.SetStateAction<CCJobInformation[]>>
    tracker: Map<string, JobTracking>
    setTracker: React.Dispatch<React.SetStateAction<Map<string, JobTracking>>>
}

interface jobDetails {
    name: string,
    type: string,
    submitDateTime: string,
    inputs: string[],
    outputs: string[]
}

export function ContextCapture(props: CccsProps) {

    const OUTPUTS = ["Cesium 3D Tiles", "OPC", "WebReady ScalableMesh", "CCOrientations"];
    const BASE_URL = "https://" + process.env.IMJS_URL_PREFIX + "api.bentley.com/contextcapture";

    const [inputs, setInputs] = React.useState<Map<string, string>>(new Map());
    const [error, setError] = React.useState<string>("");
    const [jobName, setJobName] = React.useState<string>("");
    const [showDialog, setShowDialog] = React.useState(false);
    const [curJob, setCurJob] = React.useState<jobDetails>();

    const map = new Map<string, boolean>();
    OUTPUTS.forEach(element => {
        map.set(element, false);
    });
    const [outputs, setOutputs] = React.useState<Map<string, boolean>>(map);


    useEffect(() => {
        setInterval(() => {
            const newTracker = new Map<string, JobTracking>();
            console.log("Size Jobs = " + props.tracker.size);
            [...props.tracker.keys()].forEach(async jobId => {
                const lastState = props.tracker.get(jobId);
                if (lastState != undefined && lastState.step === "Over") {
                    newTracker.set(jobId, lastState);
                }
                else{
                    const progress = await fetch(BASE_URL + "/jobs/" + jobId + "/progress", {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            "Accept": "application/vnd.bentley.v1+json",
                            "Authorization": props.accessToken,
                            "Access-Control-Allow-Origin": "*"
                        }
                    });
                    const progressJson = await progress.json();
                    if (progressJson.jobProgress.state == "Over") {
                        props.jobs.filter(j => j.id == jobId)[0].completed = true;
                        props.setJobs(props.jobs);
                    }

                    newTracker.set(jobId, {step: progressJson.jobProgress.step, percentage: parseInt(progressJson.jobProgress.percentage)});
                }

            });

            props.setTracker(newTracker);
        }, 10000);
    });

    const onJobRun = async (): Promise<void> => {
        setError("");

        // Create a new CCCS workspace
        const createWS = await fetch(BASE_URL + "/workspaces", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/vnd.bentley.v1+json",
                "Authorization": props.accessToken
            },
            body: JSON.stringify({
                name: "WS for " + jobName,
                iTwinId: process.env.IMJS_PROJECT_ID
            })
        });
        if (!createWS.ok) {
            setError("Failed to create workspace");
            return;
        }
        const wsJson = await createWS.json();
        const wsId = wsJson.workspace.id;
        console.log(wsId);

        // Create new job
        const cccsInputs = [...inputs.values()].map(e => ({
            id: e,
            description: "My inputs"
        }));
        const cccsOutputs = [...outputs.keys()].filter(out => outputs.get(out) ?? false);
        if (cccsOutputs.includes("WebReady ScalableMesh")) {
            cccsOutputs.push("3SM");
        }
        const createJob = await fetch(BASE_URL + "/jobs", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/vnd.bentley.v1+json",
                "Authorization": props.accessToken
            },
            body: JSON.stringify({
                type: "Full",
                name: jobName,
                workspaceId: wsId,
                inputs: cccsInputs,
                settings: {
                    meshQuality: "Draft",
                    processingEngines: 5,
                    outputs: cccsOutputs
                }
            })
        });

        if (!createJob.ok) {
            setError("Failed to create job");
            return;
        }
        const jobId = (await createJob.json()).job.id;

        // Submitting job
        const submitJob = await fetch(BASE_URL + "/jobs/" + jobId, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/vnd.bentley.v1+json",
                "Authorization": props.accessToken
            },
            body: JSON.stringify({
                state: "Active"
            })
        });
        if (!submitJob.ok) {
            setError("Failed to submit job");
            console.log(await submitJob.json());
            return;
        }

        const job = new CCJobInformation(jobName, jobId);
        props.jobs.push(job);
        props.setJobs(props.jobs);
        props.setTracker(new Map(props.tracker.set(jobId, {step: "", percentage: 0})));
    };

    function createCheckbox(label: string) {
        return <Checkbox key={label} className="cccs-check" label={label}
            onChange={(input: React.ChangeEvent<HTMLInputElement>) => setOutputs(new Map(outputs.set(label, input.target.checked)))} />;
    }

    function createCheckboxes() {
        return <div className="cccs-check">{OUTPUTS.flatMap((output) => createCheckbox(output))}</div>;
    }

    function disabledRun()
    {
        if (inputs.size != 2) {
            return true;
        }
        // Check inputs are filled
        if ([...inputs.values()].map(e => e.length == 0).reduce((a,b) => a||b)) {
            return true;
        }

        if (jobName.length == 0) {
            return true;
        }

        // Check if at least one output is ticked
        return ![...outputs.values()].reduce((a, b) => (a || b));
    }

    function getRadialStatus(job: CCJobInformation) {
        if (!job.completed) {
            return undefined;
        }
        if (job.success) {
            return "positive";
        }
        return "negative";
    }

    async function generateDetailsDialog(jobId: string)
    {
        const getJob = await fetch(BASE_URL + "/jobs/" + jobId, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/vnd.bentley.v1+json",
                "Authorization": props.accessToken
            }
        });
        if (!getJob.ok) {
            setError("Failed to retrive job information for " + jobId);
            return;
        }
        const jobJson = (await getJob.json()).job;
        const jd: jobDetails = {name: jobJson.name,
            type: jobJson.type,
            submitDateTime: jobJson.executionInformation.submittedDateTime,
            outputs: jobJson.jobSettings.outputs.map((x: any) => x.format),
            inputs: jobJson.inputs.map((x: any) => x.id)
        };
        setCurJob(jd);
        setShowDialog(true);
    }

    function submittedJob(job: CCJobInformation)
    {
        return <li key={job.id}><ProgressRadial status={getRadialStatus(job)} value={props.tracker.get(job.id)?.percentage} /> <a onClick={() => generateDetailsDialog(job.id)}>{job.name}</a></li>;
    }

    function submittedJobs()
    {
        return <ul className="ccs-controls-group">{props.jobs.map((job) => submittedJob(job))}</ul>;
    }

    function renderError() {
        if (error.length > 0)
            return <Alert type="negative" onClose={() => setError("")}>{error}</Alert>;
        return undefined;
    }

    function detailsDialog() {
        if (showDialog) {
            return <Dialog
                isOpen={showDialog}
                onClose={() => setShowDialog(false)}
                closeOnEsc
                closeOnExternalClick
                preventDocumentScroll
                trapFocus
                setFocus
                isDismissible
            >
                <Dialog.Main>
                    <Dialog.TitleBar titleText={"Job " + curJob?.name} />
                    <Dialog.Content>
                        <b>Type: </b>{curJob?.type}<br />
                        <b>Submit time: </b>{curJob?.submitDateTime}
                    </Dialog.Content>
                </Dialog.Main>
            </Dialog>;
        }
        return undefined;
    }

    return(
        <div>
            <h1>Inputs</h1>
            <div className="ccs-controls-group">
                <LabeledInput className="ccs-control" displayStyle="inline" label="Job Name" placeholder="Enter job name here..."
                    onChange={(input: React.ChangeEvent<HTMLInputElement>) => setJobName(input.target.value)}/>
                <LabeledInput className="ccs-control" displayStyle="inline" label="Image Collection" placeholder="Enter id here..."
                    onChange={(input: React.ChangeEvent<HTMLInputElement>) => setInputs(new Map(inputs.set("CCImageCollection", input.target.value)))}/>
                <LabeledInput className="ccs-control" displayStyle="inline" label="Orientations" placeholder="Enter id here..."
                    onChange={(input: React.ChangeEvent<HTMLInputElement>) => setInputs(new Map(inputs.set("CCOrientation", input.target.value)))}/>

                {createCheckboxes()}
                <Button className="ccs-control" startIcon={<SvgPlay />} styleType="cta" disabled={disabledRun()} onClick={onJobRun}>Run new job</Button>
            </div>

            <h1>Submitted jobs</h1>
            {submittedJobs()}

            {renderError()}

            {detailsDialog()}
        </div>
    );
}