/*---------------------------------------------------------------------------------------------
* Copyright (c) Bentley Systems, Incorporated. All rights reserved.
* See LICENSE.md in the project root for license terms and full copyright notice.
*--------------------------------------------------------------------------------------------*/

export class DataInformation {
    name: string;
    id: string;
    rdType: string;

    constructor(n: string, i: string, t: string) {
        this.name = n;
        this.id = i;
        this.rdType = t;
    }
}

export class CCJobInformation {
    name: string;
    id: string;
    completed: boolean;
    success!: boolean;

    constructor(n: string, i: string) {
        this.name = n;
        this.id = i;
        this.completed = false;
    }
}

export class JobTracking {
    step: string;
    percentage: number;

    constructor(s: string, p: number) {
        this.step = s;
        this.percentage = p;
    }
}