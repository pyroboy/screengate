import{a as t,b as s,c as n,d as a,i as e,e as r,S as o,s as i,g as c,f as u,t as f,m as l,h,j as p,k as m,l as d,o as v,q as x,r as j,D as b,n as g}from"./index.8fe49ea3.js";import{_ as H}from"./slicedToArray.f13a096f.js";import"./_commonjsHelpers.e0f9ccb2.js";import{_ as w}from"./index.2e828dd7.js";function y(t){var s,n,a,e,r,o,i=t[0].title+"",w=t[0].html+"";return document.title=s=t[0].title,{c:function(){n=c(),a=u("h1"),e=f(i),r=c(),o=u("div"),this.h()},l:function(t){n=l(t),a=h(t,"H1",{});var s=p(a);e=m(s,i),s.forEach(d),r=l(t),o=h(t,"DIV",{class:!0}),p(o).forEach(d),this.h()},h:function(){v(o,"class","content svelte-gnxal1")},m:function(t,s){x(t,n,s),x(t,a,s),j(a,e),x(t,r,s),x(t,o,s),o.innerHTML=w},p:function(t,n){var a=H(n,1)[0];1&a&&s!==(s=t[0].title)&&(document.title=s),1&a&&i!==(i=t[0].title+"")&&b(e,i),1&a&&w!==(w=t[0].html+"")&&(o.innerHTML=w)},i:g,o:g,d:function(t){t&&d(n),t&&d(a),t&&d(r),t&&d(o)}}}function T(t){var s,n,a;return w.async(function(e){for(;;)switch(e.prev=e.next){case 0:return s=t.params,t.query,e.next=3,w.awrap(this.fetch("blog/".concat(s.slug,".json")));case 3:return n=e.sent,e.next=6,w.awrap(n.json());case 6:if(a=e.sent,200!==n.status){e.next=11;break}return e.abrupt("return",{post:a});case 11:this.error(n.status,a.message);case 12:case"end":return e.stop()}},null,this)}function _(t,s,n){var a=s.post;return t.$set=function(t){"post"in t&&n(0,a=t.post)},[a]}export default(function(c){function u(t){var o;return s(this,u),o=n(this,a(u).call(this)),e(r(o),t,_,y,i,{post:0}),o}return t(u,o),u}());export{T as preload};
