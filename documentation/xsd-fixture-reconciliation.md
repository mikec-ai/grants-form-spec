# Grants.gov root XSD fixture reconciliation

Every emitted Grants.gov XML profile pins the official source URI, its native version, and the
SHA-256 of the physical source bytes. The machine-readable reconciliation is
`tests/fixtures/grants-gov-xsd/root-fixture-manifest.json`. Producer preflight requires exact
agreement among that row, the emitted profile, its root-XSD evidence record, and the physical
fixture. It rejects non-HTTPS, wrong-host, relative, system/dependency, version-drifted, duplicate,
and stale claims. The URI basename must have exactly one candidate in the fixture corpus, even if
one of several candidates happens to match the expected hash. Filename equality, equivalent XML,
and successful XSD validation do not establish byte provenance. Any normalized or transformed
copy must retain separate lineage outside the root-fixture claim and cannot satisfy this gate.
Native version is parsed from the exact official filename suffix `-V<major>.<minor>.xsd`; matching
but incorrect manifest and evidence values cannot override the version carried by the source URI.

Physical source provenance remains distinct from extraction provenance. For example, R&R Budget
10YR pins physical XSD SHA-256 `e9d004c15ffcbae04b65087cb0eff7e87b8eb8ba0ffd6bfb6aba5542e04708cc`,
while its historical extraction at revision `dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef`
retains source-set SHA-256 `cccce03554424d59b5958e4443a54db12a5a10780fbdc5df2ec25955d443fc9d`.
Neither digest is rewritten to resemble the other.

All source URIs below use `https://apply07.grants.gov/apply/forms/schemas/` followed by the
listed filename. The table is the 30-profile reconciliation; the gate regenerates its judgment from emitted
profiles and fixture bytes on every preflight.

| Form | Version | Official XSD | Physical SHA-256 | Byte-exact fixture |
|---|---:|---|---|---|
| `attachment-form` | `1.2` | `AttachmentForm_1_2-V1.2.xsd` | `c6b7f40614a2077818f5f3b5df72959f867611b887c5b888005df8adeaa5e8e9` | `attachment-form-1.2/AttachmentForm_1_2-V1.2.xsd` |
| `cd511` | `1.1` | `CD511-V1.1.xsd` | `f13c05b8e62fe1e7cf0198053f79fdd34efe4b7d10b56974d27a7dd45d013fde` | `cd511-1.1/CD511-V1.1.xsd` |
| `gg-lobbying` | `1.1` | `GG_LobbyingForm-V1.1.xsd` | `a41d88b19e240dbb5f9b13815c0426d2396414fc1af8d6ab6a96f35855a0a5f7` | `gg-lobbying-1.1/GG_LobbyingForm-V1.1.xsd` |
| `individual-sf424b` | `1.1` | `Individual_SF424B-V1.1.xsd` | `1fe96cd37f1933f1c251efbbfbafae85c2e4869359f216a645024860ee29c983` | `sf424b-1.1/Individual_SF424B-V1.1.xsd` |
| `individual-sf424d` | `1.1` | `Individual_SF424D-V1.1.xsd` | `52187d42b9ca30cf1f2f95de50be13bbd9ae333ede4b843e8c43b23db4489356` | `sf424d-family-1.1/Individual_SF424D-V1.1.xsd` |
| `mandatory-sf424b` | `1.1` | `Mandatory_SF424B-V1.1.xsd` | `bcbe0010ba734ebeb0e3b6bd331a936d716b9896446231be90a11b005faf9579` | `sf424b-1.1/Mandatory_SF424B-V1.1.xsd` |
| `mandatory-sf424d` | `1.1` | `Mandatory_SF424D-V1.1.xsd` | `6685f2c19329db0ee959e2453cbcaf749e9bb2d7f45cb96892d9a4e71d87f68d` | `sf424d-family-1.1/Mandatory_SF424D-V1.1.xsd` |
| `nifa-supplemental` | `1.2` | `NIFA_Supplemental_Info_1_2-V1.2.xsd` | `9fd2d43797ec5fe17a9c29f073295e1c459b13d39346b3422de036d51c1d69e2` | `nifa-supplemental-1.2/NIFA_Supplemental_Info_1_2-V1.2.xsd` |
| `performance-site` | `4.0` | `PerformanceSite_4_0-V4.0.xsd` | `d47dbb254b112f69dc308c01dea2fe15b29114d0e3bdc5a137d3178b5af7bc6c` | `performance-site-4.0/PerformanceSite_4_0-V4.0.xsd` |
| `phs-assignment-request` | `4.0` | `PHS_AssignmentRequestForm_4_0-V4.0.xsd` | `7e697ee33ea6f72271c0d74fc48c61f4f81faa242a712a4c73e7898f6c4ab976` | `phs-assignment-request-4.0/PHS_AssignmentRequestForm_4_0-V4.0.xsd` |
| `phs-human-subjects` | `3.0` | `PHSHumanSubjectsAndClinicalTrialsInfo_3_0-V3.0.xsd` | `29d859de80cc9febbd1599c28f5db9a3ec82bff26a4d32f4dbbc372effb56bf3` | `phs-human-subjects-3.0/PHSHumanSubjectsAndClinicalTrialsInfo_3_0-V3.0.xsd` |
| `phs-inclusion-enrollment-report` | `1.0` | `PHSInclusionEnrollmentReport-V1.0.xsd` | `3263bbfa8881c7d428958cf91de470cd19f0f6cbc11818c4752d5266bb0f53a4` | `phs-inclusion-enrollment-report-1.0/PHSInclusionEnrollmentReport-V1.0.xsd` |
| `phs398-cover-page-supplement` | `5.0` | `PHS398_CoverPageSupplement_5_0-V5.0.xsd` | `ec538c9bb5fd233c36ac73ca567d31e60779ee3df2f3c7b456d9395b3ec2dc26` | `phs398-cover-page-supplement-5.0/PHS398_CoverPageSupplement_5_0-V5.0.xsd` |
| `phs398-modular-budget` | `1.2` | `PHS398_ModularBudget_1_2-V1.2.xsd` | `f166abebd40e6912861dca5c5c4a83c7a82779f1ae67a2c0fa8b4aafc25d5bff` | `phs398-modular-budget-1.2/PHS398_ModularBudget_1_2-V1.2.xsd` |
| `phs398-research-plan` | `5.0` | `PHS398_ResearchPlan_5_0-V5.0.xsd` | `6e7171465d1f44a16eb822f8921423ceede4fa486cb0819bc5dd327121b4bb56` | `phs398-research-plan-5.0/PHS398_ResearchPlan_5_0-V5.0.xsd` |
| `rr-budget-10yr` | `3.0` | `RR_Budget10_3_0-V3.0.xsd` | `e9d004c15ffcbae04b65087cb0eff7e87b8eb8ba0ffd6bfb6aba5542e04708cc` | `rr-budget-10yr-3.0/RR_Budget10_3_0-V3.0.xsd` |
| `rr-budget` | `3.0` | `RR_Budget_3_0-V3.0.xsd` | `d474010f85819549990de65fc51292bed08ba98ac0895d0dde9513fbe855cdbc` | `rr-budget-3.0/RR_Budget_3_0-V3.0.xsd` |
| `rr-key-person-expanded` | `4.0` | `RR_KeyPersonExpanded_4_0-V4.0.xsd` | `c1522304f37bb91a1fc18f2b84656c570581969f9c1795d18352bc273d691b8b` | `rr-key-person-expanded-4.0/RR_KeyPersonExpanded_4_0-V4.0.xsd` |
| `rr-other-project-information` | `1.4` | `RR_OtherProjectInfo_1_4-V1.4.xsd` | `b2144c290ed5ad6d942e70815d195d7d6aa4e8e6c82fc3932d8540e3aa303ef5` | `rr-other-project-information-1.4/RR_OtherProjectInfo_1_4-V1.4.xsd` |
| `rr-personal-data` | `1.2` | `RR_PersonalData_1_2-V1.2.xsd` | `5f766d46d573da1f6bb326bcbc13338439ba75399ad09dee2380f65e892402cb` | `rr-personal-data-1.2/RR_PersonalData_1_2-V1.2.xsd` |
| `rr-sf424` | `5.0` | `RR_SF424_5_0-V5.0.xsd` | `f140f32afed9d7efbe30fc8f299542bbbc3121dbc87a79aa351fcf096163d3bc` | `rr-sf424-5.0/RR_SF424_5_0-V5.0.xsd` |
| `rr-sf424-multi-project-cover` | `4.0` | `RR_SF424_Multi_Project_Cover_4_0-V4.0.xsd` | `5d5599068d721e6554fa442df88711f8d9386a5fafc18b01cb1d1becc41f84e7` | `rr-sf424-multi-project-cover-4.0/RR_SF424_Multi_Project_Cover_4_0-V4.0.xsd` |
| `rr-sf424b` | `1.1` | `RRSF424_SF424B-V1.1.xsd` | `511de9a5594a739ce596a33a92d3dec1bac2a32f193a2fe6b4799b45f29ff296` | `sf424b-1.1/RRSF424_SF424B-V1.1.xsd` |
| `rr-subaward-budget-10yr-30` | `3.0` | `RR_SubawardBudget10_30_3_0-V3.0.xsd` | `0ed112b2e50f0e0c43423f690201b207f5b9c5a85349335260e4fd999f3a611a` | `rr-subaward-budget-10yr-30-3.0/RR_SubawardBudget10_30_3_0-V3.0.xsd` |
| `rr-subaward-budget-30` | `3.0` | `RR_SubawardBudget30_3_0-V3.0.xsd` | `d5d534326e8f7e4416baf98c95c1f9234c0a23628259ee2d7e3199181a24e08a` | `rr-subaward-budget-30-3.0/RR_SubawardBudget30_3_0-V3.0.xsd` |
| `rr-subaward-budget` | `3.0` | `RR_SubawardBudget_3_0-V3.0.xsd` | `e1ea95403a58ef1ade290952de3531c73e015308ca7aee6b426d4a9bcb794510` | `rr-subaward-budget-3.0/RR_SubawardBudget_3_0-V3.0.xsd` |
| `sbir-sttr-information` | `3.0` | `SBIR_STTR_Information_3_0-V3.0.xsd` | `32ed46a450c1b77d9ef64ebf2a4086ab90b076aa2d3cdfedfab8c00324adcebf` | `sbir-sttr-information-3.0/SBIR_STTR_Information_3_0-V3.0.xsd` |
| `sf424b` | `1.1` | `SF424B-V1.1.xsd` | `b0da616d262329e869b7c2a12146396fd8a279d2a1723521271c519f4571075d` | `sf424b-1.1/SF424B-V1.1.xsd` |
| `sf424c` | `2.0` | `SF424C_2_0-V2.0.xsd` | `a3ec5d6bae8173fce080709a8071787293dbe6271415d905d230c584c200982a` | `sf424c-2.0/SF424C_2_0-V2.0.xsd` |
| `sf424d` | `1.1` | `SF424D-V1.1.xsd` | `22026ea7130a01b8674e1c3ce1668e1b57d5be65498b5a76042eb80d38de77f1` | `sf424d-family-1.1/SF424D-V1.1.xsd` |
| `sflll` | `2.0` | `SFLLL_2_0-V2.0.xsd` | `fff7449d00c715efb79d83b572bc7b1ef3e8171f6a9ba841436b26242e883664` | `sflll-2.0/SFLLL_2_0-V2.0.xsd` |
