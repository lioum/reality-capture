/*---------------------------------------------------------------------------------------------
* Copyright (c) Bentley Systems, Incorporated. All rights reserved.
* See LICENSE.md in the project root for license terms and full copyright notice.
*--------------------------------------------------------------------------------------------*/

import { Button, Checkbox, LabeledInput, ProgressLinear } from "@itwin/itwinui-react";
import React, { useEffect } from "react";
import "./ContextCapture.css";


interface CccsProps {
    accessToken: string
}

function delay(s: number) {
    return new Promise( resolve => setTimeout(resolve, 1000*s) );
}

export function ContextCapture(props: CccsProps) {

    const OUTPUTS = ["Cesium", "OPC", "3SM", "CCOrientation"];

    const [inputs, setInputs] = React.useState<Map<string, string>>(new Map());
    const [outputIds, setOutputIds] = React.useState<Map<string, string>>(new Map());

    const map = new Map<string, boolean>();
    OUTPUTS.forEach(element => {
        map.set(element, false);
    });
    const [outputs, setOutputs] = React.useState<Map<string, boolean>>(map);

    const [step, setStep] = React.useState<string>("");
    const [percentage, setPercentage] = React.useState<string>("");

    const onJobRun = async (): Promise<void> => {
        //
        outputIds.clear();

        // Create a new CCCS workspace
        const baseUrl = "https://" + process.env.IMJS_URL_PREFIX + "api.bentley.com/contextcapture";
        setPercentage("0");
        setStep("Creating workspace");
        const createWS = await fetch(baseUrl + "/workspaces", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/vnd.bentley.v1+json",
                "Authorization": props.accessToken
            },
            body: JSON.stringify({
                name: "My Test App Workspace",
                iTwinId: process.env.IMJS_PROJECT_ID
            })
        });
        if (!createWS.ok) {
            setStep("Failed to create workspace");
            return;
        }
        const wsJson = await createWS.json();
        const wsId = wsJson.workspace.id;
        console.log(wsId);

        // Create new job
        setStep("Creating job");
        const cccsInputs = [...inputs.values()].map(e => ({
            id: e,
            description: "My inputs"
        }));
        const cccsOutputs = [...outputs.keys()].filter(out => outputs.get(out) ?? false);
        const createJob = await fetch(baseUrl + "/jobs", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/vnd.bentley.v1+json",
                "Authorization": props.accessToken
            },
            body: JSON.stringify({
                type: "Full",
                name: "My Test App Job",
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
            setStep("Failed to create job");
            return;
        }
        const jobId = (await createJob.json()).job.id;

        // Submitting job
        setStep("Submitting job");
        const submitJob = await fetch(baseUrl + "/jobs/" + jobId, {
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
            setStep("Failed to submit job");
            console.log(await submitJob.json());
            return;
        }

        let state = "";
        while(state !== "Over") {
            const progress = await fetch(baseUrl + "/jobs/" + jobId + "/progress", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/vnd.bentley.v1+json",
                    "Authorization": props.accessToken
                }
            });
            const progressJson = await progress.json();
            setPercentage(progressJson.jobProgress.percentage);
            state = progressJson.jobProgress.state;
            setStep(progressJson.jobProgress.step);
            //await delay(5);
        }

        setStep(state);
        const job = await fetch(baseUrl + "/jobs/" + jobId, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/vnd.bentley.v1+json",
                "Authorization": props.accessToken
            }
        });
        const outIds = (await job.json()).job.jobSettings.outputs;
        const m = new Map();
        outIds.forEach((element: { format: string; realityDataId: string; }) => {
            m.set(element.format, element.realityDataId);
        });
        setOutputIds(m);
    };

    const onJobCancel = async (): Promise<void> => {
        await fetch("http://localhost:3001/requests/cancelJobCSS", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
        });
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

        // Check if at least one output is ticked
        return ![...outputs.values()].reduce((a, b) => (a || b));
    }

    function createOutput(output: string)
    {
        return <LabeledInput className="ccs-control" displayStyle="inline" label={output} disabled={true} value={outputIds.get(output) ?? "/"}/>;
    }

    function createOutputs()
    {
        return <div className="ccs-controls-group">{[...outputIds.keys()].map((output) => createOutput(output))}</div>;
    }

    return(
        <div>
            <h1>Inputs</h1>
            <div className="ccs-controls-group">
                <LabeledInput className="ccs-control" displayStyle="inline" label="Image Collection" placeholder="Enter id here..."
                    onChange={(input: React.ChangeEvent<HTMLInputElement>) => setInputs(new Map(inputs.set("CCImageCollection", input.target.value)))}/>
                <LabeledInput className="ccs-control" displayStyle="inline" label="Orientations" placeholder="Enter id here..."
                    onChange={(input: React.ChangeEvent<HTMLInputElement>) => setInputs(new Map(inputs.set("CCOrientation", input.target.value)))}/>

                {createCheckboxes()}
                <Button className="ccs-control" disabled={disabledRun()} onClick={onJobRun}>Run</Button>
            </div>

            <div className="ccs-controls-group">
                <ProgressLinear className="ccs-progress" value={parseInt(percentage)} labels={[step, percentage + "%"]}/>
                <Button className="ccs-control" disabled={!step || step === "Done" || step === "Error"} onClick={onJobCancel}>Cancel</Button>
            </div>

            {outputIds.size > 0 && (
                <div>
                    <h1>Outputs</h1>
                    {createOutputs()}
                </div>
            )}
        </div>
    );
}