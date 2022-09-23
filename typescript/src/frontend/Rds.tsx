/*---------------------------------------------------------------------------------------------
* Copyright (c) Bentley Systems, Incorporated. All rights reserved.
* See LICENSE.md in the project root for license terms and full copyright notice.
*--------------------------------------------------------------------------------------------*/

import { Button, LabeledInput, Select, SelectOption } from "@itwin/itwinui-react";
import React, { ChangeEvent, useMemo } from "react";
import "./Rds.css";
import { ContainerClient } from "@azure/storage-blob";
import { ITwinRealityData, RealityDataAccessClient, RealityDataClientOptions } from "@itwin/reality-data-client";
import JSZip from "jszip";
import FileSaver from "file-saver";
import { DOMParser, XMLSerializer } from "@xmldom/xmldom";


export enum DataTypes {
    CCImageCollection = "CCImageCollection",
    CCOrientations = "CCOrientations",
    ContextScene = "ContextScene",
    ContextDetector = "ContextDetector",
    Cesium3DTiles = "Cesium3DTiles",
    Mesh3MX = "3MX",
    OPC = "OPC",
}

interface RdsProps {
    uploadedDataType: string;
    uploadedDataSource: string;
    uploadedDataId: string;
    downloadedDataId: string;
    downloadTargetPath: string,
    accessToken: string,
    onUploadedDataSourceChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onUploadedDataTypeChange: (type: string) => void;
    onUploadedDataIdChange: (id: string) => void;
    onDownloadedIdChange: (id: React.ChangeEvent<HTMLInputElement>) => void;
    onDownloadTargetPathChange: (path: React.ChangeEvent<HTMLInputElement>) => void;
}

const localPathToRdId: Map<string, string> = new Map();

export function Rds(props: RdsProps) {

    const [uploadProgress, setUploadProgress] = React.useState<string>("");
    const [uploadedDataName, setUploadedDataName] = React.useState<string>("");
    const ref = React.useRef<HTMLInputElement>(null);

    React.useEffect(() => {
        if (ref.current !== null) {
            ref.current.setAttribute("directory", "");
            ref.current.setAttribute("webkitdirectory", "");
        }
    }, [ref]);

    /* const mimeTypes = useMemo(
        () =>
            new Map<string, string> ([
                ["jpeg", "image/jpeg"],
                ["png", "image/png"],
                ["xml", "text/xml"],
                ["json", "application/json"]
            ]),
        []
    ); */

    const selectOptions: SelectOption<DataTypes>[] = [
        { value: DataTypes.CCImageCollection, label: "ContextCapture Image Collection" },
        { value: DataTypes.CCOrientations, label: "CCOrientations"},
        { value: DataTypes.Cesium3DTiles, label: "Cesium 3D Tiles" },
        { value: DataTypes.ContextDetector, label: "Context Detector" },
        { value: DataTypes.ContextScene, label: "Context Scene" },
        { value: DataTypes.Mesh3MX, label: "ContextCapture 3MX" },
        { value: DataTypes.OPC, label: "Web Ready Point Cloud" },
    ];

    const patch = async (toPatch: string, referenceTable: Map<string, string>, isContextScene = true): Promise<string> => {
        // Does not work
        const xmlDoc = new DOMParser().parseFromString(toPatch, "text/xml");
        const references = xmlDoc.getElementsByTagName(isContextScene ? "Reference" : "Photo");
        for (let i = 0; i < references.length; i++) {
            const referencePath = references[i].getElementsByTagName(isContextScene ? "Path" : "ImagePath");
            if(referencePath.length === 0)
                continue; // No path in reference
    
            const pathValue = referencePath[0].textContent;
            if(!pathValue)
                continue; // No text content in reference path
    
            const fileName = pathValue.split("/").pop();
            referenceTable.forEach((value: string, key: string) => {
                if(!pathValue)
                    return; // No text content in reference path
    
                /* if(pathValue.includes("../")) { // Relative path
                    const relativePath = key + "/" + pathValue;
                    const absolutePath = path.normalize(relativePath);
                    pathValue = absolutePath.replace("/lib", "");
                    pathValue = pathValue.replace(/\\/g, "/");
    
                    // For CCOrientations, remove the file name;
                    if(!isContextScene) {
                        pathValue = pathValue.substring(0, pathValue.lastIndexOf("/"));
                    }
                } */
                if(pathValue === key) {
                    // For CCOrientations, remove "rds:";
                    if(!isContextScene) {
                        referencePath[0].textContent = value.substring("rds:".length, value.length) + "/" + fileName;
                    }
                    else
                        referencePath[0].textContent = value;                   
                }
            });
        }
        const newXmlStr = new XMLSerializer().serializeToString(xmlDoc);
        return newXmlStr;
    };

    const findRootDocument = async (files: FileList, extension: string): Promise<string> => {
        let root = "";
        for(let i = 0; i < files.length; i++) {
            if(files[i].webkitRelativePath.includes(extension)) {
                root = files[i].webkitRelativePath.split("/").slice(1).join("/");
            }
        }
        return root;
    };

    const onUploadFiles = async (): Promise<void> => {
        // TODO : patch scene and orientations
        if(!props.uploadedDataType)
            return;

        const input = document.getElementById("files") as HTMLInputElement;
        let root = "";
        if(props.uploadedDataType === "Cesium3DTiles") {            
            root = await findRootDocument(input.files!, ".json");
        }
        else if(props.uploadedDataType === "OPC") {
            root = await findRootDocument(input.files!, ".opc");
        }

        const realityDataClientOptions: RealityDataClientOptions = {
            baseUrl: "https://" + process.env.IMJS_URL_PREFIX + "api.bentley.com/realitydata",
        };
        const rdaClient = new RealityDataAccessClient(realityDataClientOptions);
        const realityData = new ITwinRealityData(rdaClient, null, process.env.IMJS_PROJECT_ID);
        realityData.displayName = uploadedDataName;
        realityData.description = uploadedDataName;
        realityData.classification = "Undefined";
        realityData.rootDocument = root;
        realityData.type = props.uploadedDataType;
        const iTwinRealityData: ITwinRealityData = await rdaClient.createRealityData(props.accessToken, process.env.IMJS_PROJECT_ID, realityData);
        const realityDataId = iTwinRealityData.id;

        if(props.uploadedDataType !== "ContextScene" && props.uploadedDataType !== "CCOrientations") {
            const fileName = input.files![0].webkitRelativePath;
            localPathToRdId.set(fileName.substring(0, fileName.lastIndexOf("/")), realityDataId);
        }

        const blobUrl = await iTwinRealityData.getBlobUrl(props.accessToken, "", true);
        const containerClient = new ContainerClient(blobUrl.toString());
        for(let i = 0; i < input.files!.length; i++) {
            // remove selected folder from path
            const blobName = input.files![i].webkitRelativePath.split("/").slice(1).join("/");
            const blockBlobClient = containerClient.getBlockBlobClient(blobName);

            if(blobName.includes(".xml")) {
                let text = await input.files![i].text();
                
                if(blobName.includes("ContextScene.xml")) {
                    text = await patch(text, localPathToRdId);
                }
                else if(blobName.includes("Orientations.xml")) {
                    text = await patch(text, localPathToRdId, false);
                }         

                const blob = new Blob([text] , { type: "text/xml"});
                const uploadBlobResponse = await blockBlobClient.uploadData(blob);
            }
            else {
                const buffer = await input.files![i].arrayBuffer();
                const uploadBlobResponse = await blockBlobClient.uploadData(buffer);
            }
        }
    };

    const onTypeChange = async (select: string): Promise<void> => {
        props.onUploadedDataTypeChange(select);
    };

    const onUploadedDataNameChange = async (event: ChangeEvent<HTMLInputElement>): Promise<void> => {
        setUploadedDataName(event.target.value);
    };

    const onDownloadFiles = async (): Promise<void> => {
        //TODO : patch scene and orientations
        if(!props.downloadedDataId)
            return;

        const realityDataClientOptions: RealityDataClientOptions = {
            baseUrl: "https://" + process.env.IMJS_URL_PREFIX + "api.bentley.com/realitydata",
        };
        const rdaClient = new RealityDataAccessClient(realityDataClientOptions);
        const rd = await rdaClient.getRealityData(props.accessToken, process.env.IMJS_PROJECT_ID, props.downloadedDataId);
        const blobUrl = await rd.getBlobUrl(props.accessToken, "", true);
        const containerClient = new ContainerClient(blobUrl.toString());

        const zip = new JSZip();
        const iter = await containerClient.listBlobsFlat();
        for await (const blob of iter) 
        {
            const blobContent = await containerClient.getBlockBlobClient(blob.name).download(0);
            const blobBody = await blobContent.blobBody;
            const text = await blobBody!.text();
            zip.file(blob.name, text.toString());
        }
        zip.generateAsync({ type: "blob" }).then(function (content) {
            FileSaver.saveAs(content, rd.displayName);
        });
    };

    return(
        <div>
            <div className="rds-controls-group">
                <input className="rds-control" type="file" id="files" ref={ref} />
                <Select className="rds-control" value={props.uploadedDataType} placeholder="Type of data to be uploaded" options={selectOptions} onChange={onTypeChange}/>
                <LabeledInput className="rds-control" id="name-id" displayStyle="inline" label="Name" value={uploadedDataName} onChange={onUploadedDataNameChange}/>
                <Button className="rds-control" onClick={onUploadFiles}>Upload</Button>
                <p className="rds-control">{uploadProgress}</p>
            </div>
            <div className="rds-controls-group">
                <LabeledInput className="rds-control" id="input-id" displayStyle="inline" label="Id" value={props.uploadedDataId} disabled={true}/>
            </div>
            <hr className="rds-sep"/>
            <div className="rds-controls-group">
                <LabeledInput className="rds-control" displayStyle="inline" label="Data to download" placeholder="Id to download" onChange={props.onDownloadedIdChange}/>
                <Button className="rds-control" onClick={onDownloadFiles}>Download</Button>
            </div>
        </div>
    );
}