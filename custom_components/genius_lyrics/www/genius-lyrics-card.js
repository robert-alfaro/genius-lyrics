/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const t=window,e=t.ShadowRoot&&(void 0===t.ShadyCSS||t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),s=new WeakMap;class n{constructor(t,e,s){if(this._$cssResult$=!0,s!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const i=this.t;if(e&&void 0===t){const e=void 0!==i&&1===i.length;e&&(t=s.get(i)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),e&&s.set(i,t))}return t}toString(){return this.cssText}}const o=(t,...e)=>{const s=1===t.length?t[0]:e.reduce((e,i,s)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[s+1],t[0]);return new n(s,t,i)},r=e?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new n("string"==typeof t?t:t+"",void 0,i))(e)})(t):t;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var a;const h=window,l=h.trustedTypes,c=l?l.emptyScript:"",d=h.reactiveElementPolyfillSupport,u={toAttribute(t,e){switch(e){case Boolean:t=t?c:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},p=(t,e)=>e!==t&&(e==e||t==t),g={attribute:!0,type:String,converter:u,reflect:!1,hasChanged:p},_="finalized";class f extends HTMLElement{constructor(){super(),this._$Ei=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$El=null,this._$Eu()}static addInitializer(t){var e;this.finalize(),(null!==(e=this.h)&&void 0!==e?e:this.h=[]).push(t)}static get observedAttributes(){this.finalize();const t=[];return this.elementProperties.forEach((e,i)=>{const s=this._$Ep(i,e);void 0!==s&&(this._$Ev.set(s,i),t.push(s))}),t}static createProperty(t,e=g){if(e.state&&(e.attribute=!1),this.finalize(),this.elementProperties.set(t,e),!e.noAccessor&&!this.prototype.hasOwnProperty(t)){const i="symbol"==typeof t?Symbol():"__"+t,s=this.getPropertyDescriptor(t,i,e);void 0!==s&&Object.defineProperty(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){return{get(){return this[e]},set(s){const n=this[t];this[e]=s,this.requestUpdate(t,n,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)||g}static finalize(){if(this.hasOwnProperty(_))return!1;this[_]=!0;const t=Object.getPrototypeOf(this);if(t.finalize(),void 0!==t.h&&(this.h=[...t.h]),this.elementProperties=new Map(t.elementProperties),this._$Ev=new Map,this.hasOwnProperty("properties")){const t=this.properties,e=[...Object.getOwnPropertyNames(t),...Object.getOwnPropertySymbols(t)];for(const i of e)this.createProperty(i,t[i])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(r(t))}else void 0!==t&&e.push(r(t));return e}static _$Ep(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}_$Eu(){var t;this._$E_=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$Eg(),this.requestUpdate(),null===(t=this.constructor.h)||void 0===t||t.forEach(t=>t(this))}addController(t){var e,i;(null!==(e=this._$ES)&&void 0!==e?e:this._$ES=[]).push(t),void 0!==this.renderRoot&&this.isConnected&&(null===(i=t.hostConnected)||void 0===i||i.call(t))}removeController(t){var e;null===(e=this._$ES)||void 0===e||e.splice(this._$ES.indexOf(t)>>>0,1)}_$Eg(){this.constructor.elementProperties.forEach((t,e)=>{this.hasOwnProperty(e)&&(this._$Ei.set(e,this[e]),delete this[e])})}createRenderRoot(){var i;const s=null!==(i=this.shadowRoot)&&void 0!==i?i:this.attachShadow(this.constructor.shadowRootOptions);return((i,s)=>{e?i.adoptedStyleSheets=s.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet):s.forEach(e=>{const s=document.createElement("style"),n=t.litNonce;void 0!==n&&s.setAttribute("nonce",n),s.textContent=e.cssText,i.appendChild(s)})})(s,this.constructor.elementStyles),s}connectedCallback(){var t;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(t=this._$ES)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostConnected)||void 0===e?void 0:e.call(t)})}enableUpdating(t){}disconnectedCallback(){var t;null===(t=this._$ES)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostDisconnected)||void 0===e?void 0:e.call(t)})}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$EO(t,e,i=g){var s;const n=this.constructor._$Ep(t,i);if(void 0!==n&&!0===i.reflect){const o=(void 0!==(null===(s=i.converter)||void 0===s?void 0:s.toAttribute)?i.converter:u).toAttribute(e,i.type);this._$El=t,null==o?this.removeAttribute(n):this.setAttribute(n,o),this._$El=null}}_$AK(t,e){var i;const s=this.constructor,n=s._$Ev.get(t);if(void 0!==n&&this._$El!==n){const t=s.getPropertyOptions(n),o="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==(null===(i=t.converter)||void 0===i?void 0:i.fromAttribute)?t.converter:u;this._$El=n,this[n]=o.fromAttribute(e,t.type),this._$El=null}}requestUpdate(t,e,i){let s=!0;void 0!==t&&(((i=i||this.constructor.getPropertyOptions(t)).hasChanged||p)(this[t],e)?(this._$AL.has(t)||this._$AL.set(t,e),!0===i.reflect&&this._$El!==t&&(void 0===this._$EC&&(this._$EC=new Map),this._$EC.set(t,i))):s=!1),!this.isUpdatePending&&s&&(this._$E_=this._$Ej())}async _$Ej(){this.isUpdatePending=!0;try{await this._$E_}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var t;if(!this.isUpdatePending)return;this.hasUpdated,this._$Ei&&(this._$Ei.forEach((t,e)=>this[e]=t),this._$Ei=void 0);let e=!1;const i=this._$AL;try{e=this.shouldUpdate(i),e?(this.willUpdate(i),null===(t=this._$ES)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostUpdate)||void 0===e?void 0:e.call(t)}),this.update(i)):this._$Ek()}catch(t){throw e=!1,this._$Ek(),t}e&&this._$AE(i)}willUpdate(t){}_$AE(t){var e;null===(e=this._$ES)||void 0===e||e.forEach(t=>{var e;return null===(e=t.hostUpdated)||void 0===e?void 0:e.call(t)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$Ek(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$E_}shouldUpdate(t){return!0}update(t){void 0!==this._$EC&&(this._$EC.forEach((t,e)=>this._$EO(e,this[e],t)),this._$EC=void 0),this._$Ek()}updated(t){}firstUpdated(t){}}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var v;f[_]=!0,f.elementProperties=new Map,f.elementStyles=[],f.shadowRootOptions={mode:"open"},null==d||d({ReactiveElement:f}),(null!==(a=h.reactiveElementVersions)&&void 0!==a?a:h.reactiveElementVersions=[]).push("1.6.3");const m=window,$=m.trustedTypes,y=$?$.createPolicy("lit-html",{createHTML:t=>t}):void 0,b="$lit$",w=`lit$${(Math.random()+"").slice(9)}$`,x="?"+w,A=`<${x}>`,S=document,E=()=>S.createComment(""),C=t=>null===t||"object"!=typeof t&&"function"!=typeof t,k=Array.isArray,O="[ \t\n\f\r]",P=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,z=/-->/g,U=/>/g,H=RegExp(`>|${O}(?:([^\\s"'>=/]+)(${O}*=${O}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),j=/'/g,N=/"/g,T=/^(?:script|style|textarea|title)$/i,L=(t=>(e,...i)=>({_$litType$:t,strings:e,values:i}))(1),M=Symbol.for("lit-noChange"),R=Symbol.for("lit-nothing"),I=new WeakMap,V=S.createTreeWalker(S,129,null,!1);function B(t,e){if(!Array.isArray(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==y?y.createHTML(e):e}const D=(t,e)=>{const i=t.length-1,s=[];let n,o=2===e?"<svg>":"",r=P;for(let e=0;e<i;e++){const i=t[e];let a,h,l=-1,c=0;for(;c<i.length&&(r.lastIndex=c,h=r.exec(i),null!==h);)c=r.lastIndex,r===P?"!--"===h[1]?r=z:void 0!==h[1]?r=U:void 0!==h[2]?(T.test(h[2])&&(n=RegExp("</"+h[2],"g")),r=H):void 0!==h[3]&&(r=H):r===H?">"===h[0]?(r=null!=n?n:P,l=-1):void 0===h[1]?l=-2:(l=r.lastIndex-h[2].length,a=h[1],r=void 0===h[3]?H:'"'===h[3]?N:j):r===N||r===j?r=H:r===z||r===U?r=P:(r=H,n=void 0);const d=r===H&&t[e+1].startsWith("/>")?" ":"";o+=r===P?i+A:l>=0?(s.push(a),i.slice(0,l)+b+i.slice(l)+w+d):i+w+(-2===l?(s.push(void 0),e):d)}return[B(t,o+(t[i]||"<?>")+(2===e?"</svg>":"")),s]};class F{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let n=0,o=0;const r=t.length-1,a=this.parts,[h,l]=D(t,e);if(this.el=F.createElement(h,i),V.currentNode=this.el.content,2===e){const t=this.el.content,e=t.firstChild;e.remove(),t.append(...e.childNodes)}for(;null!==(s=V.nextNode())&&a.length<r;){if(1===s.nodeType){if(s.hasAttributes()){const t=[];for(const e of s.getAttributeNames())if(e.endsWith(b)||e.startsWith(w)){const i=l[o++];if(t.push(e),void 0!==i){const t=s.getAttribute(i.toLowerCase()+b).split(w),e=/([.?@])?(.*)/.exec(i);a.push({type:1,index:n,name:e[2],strings:t,ctor:"."===e[1]?Y:"?"===e[1]?Z:"@"===e[1]?Q:J})}else a.push({type:6,index:n})}for(const e of t)s.removeAttribute(e)}if(T.test(s.tagName)){const t=s.textContent.split(w),e=t.length-1;if(e>0){s.textContent=$?$.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],E()),V.nextNode(),a.push({type:2,index:++n});s.append(t[e],E())}}}else if(8===s.nodeType)if(s.data===x)a.push({type:2,index:n});else{let t=-1;for(;-1!==(t=s.data.indexOf(w,t+1));)a.push({type:7,index:n}),t+=w.length-1}n++}}static createElement(t,e){const i=S.createElement("template");return i.innerHTML=t,i}}function G(t,e,i=t,s){var n,o,r,a;if(e===M)return e;let h=void 0!==s?null===(n=i._$Co)||void 0===n?void 0:n[s]:i._$Cl;const l=C(e)?void 0:e._$litDirective$;return(null==h?void 0:h.constructor)!==l&&(null===(o=null==h?void 0:h._$AO)||void 0===o||o.call(h,!1),void 0===l?h=void 0:(h=new l(t),h._$AT(t,i,s)),void 0!==s?(null!==(r=(a=i)._$Co)&&void 0!==r?r:a._$Co=[])[s]=h:i._$Cl=h),void 0!==h&&(e=G(t,h._$AS(t,e.values),h,s)),e}class q{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){var e;const{el:{content:i},parts:s}=this._$AD,n=(null!==(e=null==t?void 0:t.creationScope)&&void 0!==e?e:S).importNode(i,!0);V.currentNode=n;let o=V.nextNode(),r=0,a=0,h=s[0];for(;void 0!==h;){if(r===h.index){let e;2===h.type?e=new W(o,o.nextSibling,this,t):1===h.type?e=new h.ctor(o,h.name,h.strings,this,t):6===h.type&&(e=new X(o,this,t)),this._$AV.push(e),h=s[++a]}r!==(null==h?void 0:h.index)&&(o=V.nextNode(),r++)}return V.currentNode=S,n}v(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class W{constructor(t,e,i,s){var n;this.type=2,this._$AH=R,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cp=null===(n=null==s?void 0:s.isConnected)||void 0===n||n}get _$AU(){var t,e;return null!==(e=null===(t=this._$AM)||void 0===t?void 0:t._$AU)&&void 0!==e?e:this._$Cp}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===(null==t?void 0:t.nodeType)&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=G(this,t,e),C(t)?t===R||null==t||""===t?(this._$AH!==R&&this._$AR(),this._$AH=R):t!==this._$AH&&t!==M&&this._(t):void 0!==t._$litType$?this.g(t):void 0!==t.nodeType?this.$(t):(t=>k(t)||"function"==typeof(null==t?void 0:t[Symbol.iterator]))(t)?this.T(t):this._(t)}k(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}$(t){this._$AH!==t&&(this._$AR(),this._$AH=this.k(t))}_(t){this._$AH!==R&&C(this._$AH)?this._$AA.nextSibling.data=t:this.$(S.createTextNode(t)),this._$AH=t}g(t){var e;const{values:i,_$litType$:s}=t,n="number"==typeof s?this._$AC(t):(void 0===s.el&&(s.el=F.createElement(B(s.h,s.h[0]),this.options)),s);if((null===(e=this._$AH)||void 0===e?void 0:e._$AD)===n)this._$AH.v(i);else{const t=new q(n,this),e=t.u(this.options);t.v(i),this.$(e),this._$AH=t}}_$AC(t){let e=I.get(t.strings);return void 0===e&&I.set(t.strings,e=new F(t)),e}T(t){k(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,s=0;for(const n of t)s===e.length?e.push(i=new W(this.k(E()),this.k(E()),this,this.options)):i=e[s],i._$AI(n),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){var i;for(null===(i=this._$AP)||void 0===i||i.call(this,!1,!0,e);t&&t!==this._$AB;){const e=t.nextSibling;t.remove(),t=e}}setConnected(t){var e;void 0===this._$AM&&(this._$Cp=t,null===(e=this._$AP)||void 0===e||e.call(this,t))}}class J{constructor(t,e,i,s,n){this.type=1,this._$AH=R,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=n,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=R}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(t,e=this,i,s){const n=this.strings;let o=!1;if(void 0===n)t=G(this,t,e,0),o=!C(t)||t!==this._$AH&&t!==M,o&&(this._$AH=t);else{const s=t;let r,a;for(t=n[0],r=0;r<n.length-1;r++)a=G(this,s[i+r],e,r),a===M&&(a=this._$AH[r]),o||(o=!C(a)||a!==this._$AH[r]),a===R?t=R:t!==R&&(t+=(null!=a?a:"")+n[r+1]),this._$AH[r]=a}o&&!s&&this.j(t)}j(t){t===R?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=t?t:"")}}class Y extends J{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===R?void 0:t}}const K=$?$.emptyScript:"";class Z extends J{constructor(){super(...arguments),this.type=4}j(t){t&&t!==R?this.element.setAttribute(this.name,K):this.element.removeAttribute(this.name)}}class Q extends J{constructor(t,e,i,s,n){super(t,e,i,s,n),this.type=5}_$AI(t,e=this){var i;if((t=null!==(i=G(this,t,e,0))&&void 0!==i?i:R)===M)return;const s=this._$AH,n=t===R&&s!==R||t.capture!==s.capture||t.once!==s.once||t.passive!==s.passive,o=t!==R&&(s===R||n);n&&this.element.removeEventListener(this.name,this,s),o&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){var e,i;"function"==typeof this._$AH?this._$AH.call(null!==(i=null===(e=this.options)||void 0===e?void 0:e.host)&&void 0!==i?i:this.element,t):this._$AH.handleEvent(t)}}class X{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){G(this,t)}}const tt=m.litHtmlPolyfillSupport;null==tt||tt(F,W),(null!==(v=m.litHtmlVersions)&&void 0!==v?v:m.litHtmlVersions=[]).push("2.8.0");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var et,it;class st extends f{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var t,e;const i=super.createRenderRoot();return null!==(t=(e=this.renderOptions).renderBefore)&&void 0!==t||(e.renderBefore=i.firstChild),i}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{var s,n;const o=null!==(s=null==i?void 0:i.renderBefore)&&void 0!==s?s:e;let r=o._$litPart$;if(void 0===r){const t=null!==(n=null==i?void 0:i.renderBefore)&&void 0!==n?n:null;o._$litPart$=r=new W(e.insertBefore(E(),t),t,void 0,null!=i?i:{})}return r._$AI(t),r})(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),null===(t=this._$Do)||void 0===t||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this._$Do)||void 0===t||t.setConnected(!1)}render(){return M}}st.finalized=!0,st._$litElement$=!0,null===(et=globalThis.litElementHydrateSupport)||void 0===et||et.call(globalThis,{LitElement:st});const nt=globalThis.litElementPolyfillSupport;null==nt||nt({LitElement:st}),(null!==(it=globalThis.litElementVersions)&&void 0!==it?it:globalThis.litElementVersions=[]).push("3.3.3");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const ot=2;class rt{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,i){this._$Ct=t,this._$AM=e,this._$Ci=i}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */class at extends rt{constructor(t){if(super(t),this.et=R,t.type!==ot)throw Error(this.constructor.directiveName+"() can only be used in child bindings")}render(t){if(t===R||null==t)return this.ft=void 0,this.et=t;if(t===M)return t;if("string"!=typeof t)throw Error(this.constructor.directiveName+"() called with a non-string value");if(t===this.et)return this.ft;this.et=t;const e=[t];return e.raw=e,this.ft={_$litType$:this.constructor.resultType,strings:e,values:[]}}}at.directiveName="unsafeHTML",at.resultType=1;const ht=(t=>(...e)=>({_$litDirective$:t,values:e}))(at);console.info("%c GENIUS-LYRICS-CARD %c 1.0.0 ","color: white; background: #1db954; font-weight: 700;","color: #1db954; background: white; font-weight: 700;");customElements.define("genius-lyrics-card",class extends st{constructor(){super(...arguments),this.config={}}static get properties(){return{hass:{type:Object},config:{type:Object},_stateObj:{type:Object}}}_renderPyongIcon(){return L`<svg class="pyong-icon" viewBox="0 0 11.37 22" aria-hidden="true"><path d="M0 7l6.16-7 3.3 7H6.89S5.5 12.1 5.5 12.17h5.87L6.09 22l.66-7H.88l2.89-8z"></path></svg>`}_isPyongUiEnabled(){return false}static getConfigElement(){return document.createElement("genius-lyrics-card-editor")}static getStubConfig(){return{entity:"",show_image:!0,show_details:!0,show_stats:!0,stats_position:"header",show_font_controls:!0,font_size:14,max_height:400,show_pyong_button:!0,show_genius_button:!0}}setConfig(t){if(!t.entity)throw new Error("You must specify an entity (Genius Lyrics sensor)");this.config={show_image:!0,show_details:!0,show_stats:!0,stats_position:"header",show_font_controls:!0,font_size:14,max_height:400,show_pyong_button:!0,show_genius_button:!0,...t}}_getFontSize(){const t=parseInt(this.config.font_size,10);return Number.isNaN(t)?14:Math.min(30,Math.max(10,t))}_updateCardConfig(t){this.config=t,this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:t},bubbles:!0,composed:!0})),this.requestUpdate()}_changeFontSize(t){const e=Math.min(30,Math.max(10,this._getFontSize()+t));e!==this._getFontSize()&&this._updateCardConfig({...this.config,font_size:e})}_decreaseFontSize(){this._changeFontSize(-1)}_increaseFontSize(){this._changeFontSize(1)}shouldUpdate(){return Boolean(this.config)}updated(t){if(t.has("hass")&&this.hass&&this.config){const e=t.get("hass"),i=e?.states?.[this.config.entity],s=this.hass.states[this.config.entity];i!==s&&(this._stateObj=s)}}getCardSize(){return this._hasLyrics()?4:1}_hasLyrics(){if(!this._stateObj)return!1;const t=this._getLyrics();return!(!t||!t.trim())}_getLyrics(){const t=this._stateObj?.attributes?.lyrics||this._stateObj?.attributes?.media_lyrics||this._stateObj?.state||"";return"string"==typeof t?t.trimStart().trimEnd():""}_getArtist(){return this._stateObj?.attributes?.artist||this._stateObj?.attributes?.media_artist||""}_getTitle(){return this._stateObj?.attributes?.title||this._stateObj?.attributes?.media_title||""}_getImage(){return this._stateObj?.attributes?.media_image||this._stateObj?.attributes?.entity_picture||this._stateObj?.attributes?.song_art||""}_getPyongs(){return this._stateObj?.attributes?.pyong_count??this._stateObj?.attributes?.media_pyong_count??null}_getHot(){return this._stateObj?.attributes?.stats_hot??this._stateObj?.attributes?.media_stats_hot??null}_getGeniusUrl(){return this._stateObj?.attributes?.song_url||this._stateObj?.attributes?.genius_url||null}_getAnnotations(){const t=this._stateObj?.attributes?.annotations||this._stateObj?.attributes?.media_annotations;if(t&&"object"==typeof t)return this._normalizeAnnotations(t);if(this.config.annotations&&"object"==typeof this.config.annotations)return this._normalizeAnnotations(this.config.annotations);if(this.config.annotations_entity&&this.hass){const t=this.hass.states[this.config.annotations_entity];if(t){let e=this.config.annotations_attribute?t.attributes?.[this.config.annotations_attribute]:t.state;if("string"==typeof e)try{e=JSON.parse(e)}catch{e=null}if(e&&"object"==typeof e)return this._normalizeAnnotations(e)}}return{}}_normalizeAnnotations(t){const e={};for(const[i,s]of Object.entries(t))Array.isArray(s)?e[i]=s.map(String):null!=s&&(e[i]=[String(s)]);return e}_handlePyong(){if(!this.hass)return;const t=this._getArtist(),e=this._getTitle(),i=`glc-pyong:${t}::${e}`,s=!("1"===localStorage.getItem(i));localStorage.setItem(i,s?"1":"0"),this.hass.connection.sendMessage({type:"fire_event",event_type:"genius_lyrics_pyong",event_data:{artist:t,title:e,pyonged:s}}),this.requestUpdate()}_isPyonged(){const t=`glc-pyong:${this._getArtist()}::${this._getTitle()}`;return"1"===localStorage.getItem(t)}_handleOpenGenius(){const t=this._getGeniusUrl();if(t)return void window.open(t,"_blank","noopener,noreferrer");const e=this._getArtist(),i=this._getTitle();if(!e&&!i)return;const s=encodeURIComponent(`${e} ${i}`.trim());window.open(`https://genius.com/search?q=${s}`,"_blank","noopener,noreferrer")}_applyAnnotations(t){const e=this._getAnnotations();if(!t||!e||0===Object.keys(e).length)return this._escapeHtml(t);let i=t;const s=new Set,n=Object.keys(e).sort((t,e)=>e.length-t.length);for(const t of n){if(s.has(t)||!t.trim())continue;const n=new RegExp(this._escapeRegExp(t),"m");if(!i.match(n))continue;const o=e[t]||[],r=o.join("\n\n"),a=JSON.stringify(o).replace(/</g,"\\u003c").replace(/>/g,"\\u003e"),h=`<span class="annotated" data-line="${this._escapeHtml(t)}" data-anno="${this._escapeHtml(r)}" data-anno-raw='${a}'>${this._escapeHtml(t)}</span>`;i=i.replace(n,h),s.add(t)}return i.replace(/\n/g,"<br>")}_escapeRegExp(t){return t.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")}_escapeHtml(t){return String(t||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\"/g,"&quot;").replace(/'/g,"&#039;")}_handleAnnotationClick(t){const e=t.target,i=e?.closest(".annotated");if(!i)return;const s=i.getAttribute("data-line")||"",n=i.getAttribute("data-anno-raw")||"[]";let o=[];try{o=JSON.parse(n)}catch{o=[]}this._openAnnotationModal(s,o)}_openAnnotationModal(t,e){const i=new CustomEvent("show-dialog",{detail:{dialogTag:"genius-lyrics-annotation-dialog",dialogImport:()=>Promise.resolve(),dialogParams:{line:t,annotations:e}},bubbles:!0,composed:!0});this.dispatchEvent(i);const s=e.join("\n\n");s&&setTimeout(()=>alert(`"${t}"\n\n${s}`),100)}render(){if(!this.hass||!this.config)return L``;const t=this.hass.states[this.config.entity];if(!t)return L`
        <ha-card>
          <div class="warning">Entity ${this.config.entity} not found</div>
        </ha-card>
      `;this._stateObj=t;const e=t.state?.toLowerCase(),i=t.attributes?.media_lyrics,s="string"==typeof i&&"lyrics not found"===i.trim().toLowerCase();return"off"===e&&s?this._renderLyricsNotFound():"off"===e||"unavailable"===e||"unknown"===e?this._renderOffState():this._hasLyrics()?this._renderWithLyrics():this._renderNoLyrics()}_renderOffState(){return L`
      <ha-card>
        <div class="no-lyrics">
          <ha-icon icon="mdi:power-off"></ha-icon>
          <div class="no-lyrics-text">No media playing</div>
        </div>
      </ha-card>
    `}_renderNoLyrics(){return L`
      <ha-card>
        <div class="no-lyrics">
          <ha-icon icon="mdi:music-note-off"></ha-icon>
          <div class="no-lyrics-text">No lyrics available</div>
        </div>
      </ha-card>
    `}_renderLyricsNotFound(){return L`
      <ha-card>
        <div class="no-lyrics">
          <ha-icon icon="mdi:file-search-outline"></ha-icon>
          <div class="no-lyrics-text">No lyrics found</div>
        </div>
      </ha-card>
    `}_renderWithLyrics(){const t=this._getArtist(),e=this._getTitle(),i=this._getImage(),s=this._getLyrics(),n=this._getPyongs(),o=this._getHot(),r=this.config.show_image&&i,a=this.config.show_details,h=!1!==this.config.show_stats,l=h&&"bottom_left"===this.config.stats_position,c=h&&!l,d=!1!==this.config.show_font_controls,u=this._isPyonged(),p=this._getFontSize(),g=this._applyAnnotations(s),_=parseInt(this.config.max_height,10),f=_>0?`max-height: ${_}px; overflow-y: auto; font-size: ${p}px;`:`font-size: ${p}px;`;return L`
      <ha-card>
        <div class="card-content">
          <div class="header">
            ${r?L`
                  <img class="cover" src="${i}" alt="${e}" />
                `:""}
            ${a||c?L`
                  <div class="meta">
                    ${a?L`<div class="title" title="${e||"-"}">${e||"-"}</div>`:""}
                    ${a&&t?L`<div class="artist">${t}</div>`:""}
                    ${!c||null===n&&!0!==o?"":L`
                          <div class="stats">
                            ${null!==n?L`<span title="Pyong count">${this._renderPyongIcon()}${n}</span>`:""}
                            ${!0===o?L`<span title="Hot on Genius">🔥 Hot</span>`:""}
                          </div>
                        `}
                  </div>
                `:""}
          </div>

          <div class="lyrics" style="${f}" @click="${this._handleAnnotationClick}">${g?ht(g):""}</div>

          ${l||d||this._isPyongUiEnabled()&&this.config.show_pyong_button||this.config.show_genius_button?L`
                <div class="actions">
                  ${l||d?L`
                        <div class="left-controls">
                          ${!l||null===n&&!0!==o?"":L`
                                <div class="stats bottom-stats">
                                  ${null!==n?L`<span title="Pyong count">${this._renderPyongIcon()}${n}</span>`:""}
                                  ${!0===o?L`<span title="Hot on Genius">🔥 Hot</span>`:""}
                                </div>
                              `}
                          ${d?L`
                                <div class="font-controls">
                                  <mwc-button dense outlined @click="${this._increaseFontSize}" class="font-btn" title="Increase font size">
                                    <ha-icon icon="mdi:format-font-size-increase"></ha-icon>
                                  </mwc-button>
                                  <mwc-button dense outlined @click="${this._decreaseFontSize}" class="font-btn" title="Decrease font size">
                                    <ha-icon icon="mdi:format-font-size-decrease"></ha-icon>
                                  </mwc-button>
                                </div>
                              `:""}
                        </div>
                      `:""}
                  ${this._isPyongUiEnabled()&&this.config.show_pyong_button?L`
                        <mwc-button
                          dense
                          outlined
                          @click="${this._handlePyong}"
                          class="pyong-btn ${u?"pyonged":""}"
                        >
                          ${this._renderPyongIcon()}
                          ${u?"Pyonged":"Pyong"}
                        </mwc-button>
                      `:""}
                  ${this.config.show_genius_button?L`
                        <mwc-button dense outlined @click="${this._handleOpenGenius}" class="genius-btn">
                          <ha-icon icon="mdi:open-in-new"></ha-icon>
                          Open in Genius
                        </mwc-button>
                      `:""}
                </div>
              `:""}
        </div>
      </ha-card>
    `}static get styles(){return o`
      :host {
        display: block;
      }

      ha-card {
        height: 100%;
      }

      .card-content {
        padding: 16px;
      }

      .warning {
        padding: 16px;
        color: var(--error-color, #db4437);
        font-weight: 500;
      }

      .no-lyrics {
        padding: 24px;
        text-align: center;
        opacity: 0.6;
      }

      .no-lyrics ha-icon {
        --mdc-icon-size: 48px;
        color: var(--secondary-text-color);
      }

      .no-lyrics-text {
        margin-top: 8px;
        font-size: 14px;
        color: var(--secondary-text-color);
      }

      .header {
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 16px;
        margin-bottom: 16px;
        align-items: start;
      }

      .cover {
        width: 80px;
        height: 80px;
        border-radius: var(--ha-card-border-radius, 12px);
        object-fit: cover;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
      }

      .meta {
        display: flex;
        flex-direction: column;
        gap: 4px;
        min-width: 0;
      }

      .title {
        font-size: 18px;
        font-weight: 600;
        color: var(--primary-text-color);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .artist {
        font-size: 14px;
        color: var(--secondary-text-color);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .stats {
        display: flex;
        gap: 12px;
        font-size: 12px;
        color: var(--secondary-text-color);
        margin-top: 4px;
      }

      .stats span {
        display: inline-flex;
        align-items: center;
        gap: 4px;
      }

      .stats .pyong-icon {
        color: var(--primary-text-color);
      }

      .bottom-stats {
        margin-top: 0;
      }

      .lyrics {
        background: var(--secondary-background-color);
        border-radius: var(--ha-card-border-radius, 12px);
        padding: 16px;
        line-height: 1.6;
        white-space: pre-wrap;
        word-wrap: break-word;
        font-size: 14px;
        color: var(--primary-text-color);
        margin-bottom: 12px;
        user-select: text;
        -webkit-user-select: text;
        -moz-user-select: text;
        -ms-user-select: text;
        cursor: text;
      }

      .lyrics::-webkit-scrollbar {
        width: 8px;
      }

      .lyrics::-webkit-scrollbar-track {
        background: transparent;
      }

      .lyrics::-webkit-scrollbar-thumb {
        background: var(--divider-color);
        border-radius: 4px;
      }

      .lyrics::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-text-color);
      }

      .annotated {
        background: linear-gradient(transparent 65%, rgba(255, 193, 7, 0.3) 0);
        cursor: help;
        position: relative;
        padding: 0 2px;
      }

      .annotated:hover {
        background: linear-gradient(transparent 65%, rgba(255, 193, 7, 0.5) 0);
      }

      @media (hover: hover) {
        .annotated[data-anno]:hover::after {
          content: attr(data-anno);
          position: absolute;
          left: 0;
          top: 100%;
          z-index: 1000;
          min-width: 200px;
          max-width: 400px;
          white-space: pre-wrap;
          padding: 12px;
          margin-top: 8px;
          background: var(--card-background-color);
          border: 1px solid var(--divider-color);
          border-radius: 8px;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
          color: var(--primary-text-color);
          font-size: 13px;
          line-height: 1.5;
          pointer-events: none;
        }
      }

      .actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }

      .actions .pyong-btn {
        margin-right: auto;
      }

      .left-controls {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        margin-right: auto;
      }

      .font-controls {
        display: inline-flex;
        align-items: center;
        gap: 6px;
      }

      .font-btn {
        min-width: 0;
      }

      .actions .genius-btn {
        margin-left: auto;
      }

      mwc-button {
        --mdc-theme-primary: var(--primary-color);
        --mdc-typography-button-font-size: 13px;
        --mdc-button-horizontal-padding: 14px;
        transition: background-color 140ms ease, box-shadow 140ms ease, transform 140ms ease;
        border-radius: 10px;
        padding: 3px;
      }

      mwc-button ha-icon {
        --mdc-icon-size: 18px;
        margin-right: 4px;
      }

      .pyong-icon {
        display: inline-block;
        width: 18px;
        height: 18px;
        fill: currentColor;
        vertical-align: text-bottom;
      }

      mwc-button.pyonged {
        --mdc-theme-primary: var(--error-color, #db4437);
      }

      .pyong-btn:hover,
      .genius-btn:hover,
      .font-btn:hover,
      .pyong-btn:focus-within,
      .genius-btn:focus-within,
      .font-btn:focus-within {
        background-color: rgba(203, 203, 203, 0.1);
        box-shadow: 0 1px 8px rgba(0, 0, 0, 0.12);
        transform: translateY(-1px);
      }

      .pyong-btn.pyonged:hover,
      .pyong-btn.pyonged:focus-within {
        background-color: rgba(203, 203, 203, 0.1);
      }

      @media (max-width: 600px) {
        .header {
          grid-template-columns: 60px 1fr;
          gap: 12px;
        }

        .cover {
          width: 60px;
          height: 60px;
        }

        .title {
          font-size: 16px;
        }

        .artist {
          font-size: 13px;
        }
      }
    `}});customElements.define("genius-lyrics-card-editor",class extends st{constructor(){super(...arguments),this.config={}}static get properties(){return{hass:{type:Object},config:{type:Object}}}setConfig(t){this.config={show_image:!0,show_details:!0,show_stats:!0,stats_position:"header",show_font_controls:!0,font_size:14,max_height:400,show_pyong_button:!0,show_genius_button:!0,...t}}configChanged(t){this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:t},bubbles:!0,composed:!0}))}_valueChanged(t){if(!this.config||!this.hass)return;const e=t.target,i=e.configValue;if(!i)return;let s=t.detail?.value??e.value;if("checkbox"===e.type||"HA-SWITCH"===e.tagName?s=e.checked:"number"===e.type&&(s=parseInt(e.value,10)),this.config[i]===s)return;const n={...this.config,[i]:s};this.config=n,this.configChanged(n),this.requestUpdate()}_statsPositionChanged(t){if(!this.config||!this.hass)return;const e=t.target,i={...this.config,stats_position:e.checked?"bottom_left":"header"};this.config=i,this.configChanged(i),this.requestUpdate()}render(){return this.hass&&this.config?L`
      <div class="card-config">
        <ha-entity-picker
          .hass="${this.hass}"
          .value="${this.config.entity||""}"
          .configValue="${"entity"}"
          .label="${"Entity (Required)"}"
          .required="${!0}"
          allow-custom-entity
          @value-changed="${this._valueChanged}"
        ></ha-entity-picker>

        <div class="side-by-side">
          <ha-formfield label="Show Album Art">
            <ha-switch
              .checked="${!1!==this.config.show_image}"
              .configValue="${"show_image"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>

          <ha-formfield label="Show Details (Artist/Title)">
            <ha-switch
              .checked="${!1!==this.config.show_details}"
              .configValue="${"show_details"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>
        </div>

        <div class="side-by-side">
          <ha-formfield label="Show Stats (Pyongs/Hot)">
            <ha-switch
              .checked="${!1!==this.config.show_stats}"
              .configValue="${"show_stats"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>

          <ha-formfield label="Show Font Size Buttons">
            <ha-switch
              .checked="${!1!==this.config.show_font_controls}"
              .configValue="${"show_font_controls"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>
        </div>

        <div class="side-by-side">
          <ha-formfield label="Place Stats in Lower Left">
            <ha-switch
              .checked="${"bottom_left"===this.config.stats_position}"
              @change="${this._statsPositionChanged}"
            ></ha-switch>
          </ha-formfield>
        </div>

        <ha-textfield
          label="Max Height (px) - Set to 0 for unlimited"
          type="number"
          min="0"
          max="2000"
          step="1"
          .value="${String(this.config.max_height??400)}"
          .configValue="${"max_height"}"
          @change="${this._valueChanged}"
        ></ha-textfield>

        <ha-textfield
          label="Lyrics Font Size (px)"
          type="number"
          min="10"
          max="30"
          step="1"
          .value="${String(this.config.font_size??14)}"
          .configValue="${"font_size"}"
          @change="${this._valueChanged}"
        ></ha-textfield>

        <div class="side-by-side">
          <ha-formfield label="Show Genius Button">
            <ha-switch
              .checked="${!1!==this.config.show_genius_button}"
              .configValue="${"show_genius_button"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>
        </div>
      </div>
    `:L``}static get styles(){return o`
      .card-config {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      .side-by-side {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
      }

      ha-formfield {
        display: flex;
        align-items: center;
        padding: 8px 0;
      }
    `}}),window.customCards=window.customCards||[],window.customCards.push({type:"genius-lyrics-card",name:"Genius Lyrics Card",description:"Display song lyrics from Genius with annotations support",preview:!0,documentationURL:"https://github.com/robert-alfaro/genius-lyrics"});
//# sourceMappingURL=genius-lyrics-card.js.map
