# NaukriGulf iOS — Knowledge Base

Generated: 2026-11-02T22:11:28

## File counts

| Kind | Files |
|---|---|
| plist | 9 |
| storyboard | 14 |
| strings | 2 |
| swift | 1059 |
| xib | 310 |

## Features (by folder under `NaukriGulf/Classes/Controllers`)

| Feature | Files | ViewControllers | ViewModels |
|---|---|---|---|
| JobsTab | 274 | 27 | 18 |
| ProfileTab | 194 | 28 | 24 |
| Shared/CoreData | 126 | 0 | 0 |
| ActivityTab | 106 | 9 | 6 |
| CommonCellandView | 105 | 1 | 0 |
| MoreTab | 101 | 16 | 14 |
| Shared/ThirdParty | 84 | 2 | 2 |
| RegistrationFlow | 64 | 22 | 12 |
| Shared/NetworkingSwift | 51 | 0 | 0 |
| PushdownFlow | 46 | 2 | 8 |
| Shared/Extensions | 26 | 0 | 0 |
| NewResman | 25 | 11 | 6 |
| ExploreTab | 23 | 1 | 1 |
| LoginClass | 19 | 5 | 3 |
| Shared/Utility | 17 | 0 | 0 |
| Shared/CommonClass | 16 | 2 | 0 |
| CommonInputModels | 15 | 0 | 0 |
| Shared/ExternalLib | 15 | 1 | 0 |
| Shared/HelperClass | 14 | 0 | 0 |
| Shared/Resources | 13 | 0 | 0 |
| Shared/DropDownsUtil | 11 | 5 | 0 |
| UnRegFlow | 8 | 2 | 2 |
| CommonControllers | 7 | 4 | 1 |
| Shared/Base | 7 | 2 | 0 |
| NavigationBarViews | 4 | 0 | 0 |
| Shared/Tabs | 4 | 4 | 0 |
| Shared/DataManagerClasses | 2 | 0 | 0 |
| Shared/NotificationService | 2 | 0 | 0 |
| EventPageFlow | 1 | 0 | 0 |
| NGDocumentPreviewViewController.swift | 1 | 1 | 0 |
| NGTabsControllerClass.swift | 1 | 0 | 0 |
| Shared/AppApiSecurityHeader.swift | 1 | 0 | 0 |
| Shared/AppDelegate.swift | 1 | 0 | 0 |
| Shared/AppIntent | 1 | 0 | 0 |
| Shared/BGTasksHelper.swift | 1 | 0 | 0 |
| Shared/BaseViewController.swift | 1 | 1 | 0 |
| Shared/InitialViewController.swift | 1 | 1 | 0 |
| Shared/KeychainHelper.swift | 1 | 0 | 0 |
| Shared/LaunchScreen | 1 | 1 | 0 |
| Shared/NaukriGulf | 1 | 0 | 0 |
| Shared/TestingFlow | 1 | 0 | 0 |
| Shared/ar.lproj | 1 | 0 | 0 |
| Shared/en.lproj | 1 | 0 | 0 |

## API endpoints (121)

| Enum | Case | Method | Path |
|---|---|---|---|
| ActivityEndPoint | getActivityListing | ? | `/ngaggregator/user` |
| ActivityEndPoint | getEmployerActionApi | ? | `/mynaukrigulf/JobseekerService/v1/user/employerActivity` |
| ActivityEndPoint | getSearchAppearance | ? | `/mynaukrigulf/JobseekerService/v1/user/searchAppearance` |
| ActivityEndPoint | getWhatmaDetailInfo | ? | `/spapply/jobapplier/user/v1/applicationdetails` |
| ActivityEndPoint | getWhatmaEasyAppliedList | ? | `/spapply/jobapplier/user/v1/easyApplyList` |
| ActivityEndPoint | getWhatmaExternalAppliedList | ? | `/spapply/jobapplier/user/v1/webdetails` |
| ApplyEndPoints | applyByEmail | ? | `/spapi/jobs/jobEmail` |
| ApplyEndPoints | easyApply | ? | `/spapply/jobapplier/apply/v2` |
| ApplyEndPoints | unregApply | ? | `/spapply/jobapplier/unreg/apply/v2` |
| CustomJobAlertEndPoints | deleteCustomJobAlert | POST | `/spapi/alerts/delete` |
| CustomJobAlertEndPoints | fetchAllCustomJobAlertList | GET | `/spapi/alerts` |
| CustomJobAlertEndPoints | getMatchingAlert | POST | `/spapi/alerts/matchingAlert` |
| CustomJobAlertEndPoints | replaceCustomJobAlert | POST | `/spapi/alerts/replace/` |
| CustomJobAlertEndPoints | saveNewCustomAlert | POST | `/spapi/alerts` |
| CustomJobAlertEndPoints | updateCustomJobAlert | POST | `/spapi/alerts/update` |
| DropDownEndPoints | checkForDropdownDataVersionUpdate | GET | `/dropdown-services/v0/dropdowns/version` |
| DropDownEndPoints | getCombinedValidationMappedData | GET | `/s/2/200/j/combinedValidator.json` |
| DropDownEndPoints | getCompIAMappedData | GET | `/s/2/200/j/compWithIndAreaSugg.json` |
| DropDownEndPoints | getDesigFAMappedData | GET | `/s/2/200/j/desigWithFAreaSugg.json` |
| DropDownEndPoints | getDropdownDataByDDName | GET | `/dropdown-services/v0/dropdowns/\(ddName)/items` |
| DynamicLinkEndpoint | fetchClickAndTrack | POST | `/cloudgateway-ccs/url-shortener-services/v0/track/click-track` |
| DynamicLinkEndpoint | fetchGetAndTrack | POST | `/cloudgateway-ccs/url-shortener-services/v0/track/get-track` |
| ExchangeEndPoint | decryptEmailToken | ? | `/nglogin/token/_decrypt` |
| ExchangeEndPoint | getAtRtForConmailer | ? | `/nglogin/user/exchangeToken` |
| ExchangeEndPoint | getConmailerFromAT | ? | `/nglogin/user/self/authToken` |
| ExchangeEndPoint | verifiyEmailWithToken | ? | `/nglogin/user/emailVerificationLoginApp` |
| ExploreEndPoint | getExploreTabData | ? | `/careertips/api/postsList` |
| ExploreEndPoint | postSubmitPollResponseForLoggedIn | ? | `/ngpolls/central-poll-services/v0/poll/self/interact` |
| ExploreEndPoint | postSubmitPollResponseForLoggedOut | ? | `/ngpolls/central-poll-services/v0/poll/public/interact` |
| FeedBackEndPoints | newPostUserFeedBack | POST | `/ngprofile/loggedInUserFeedback/self` |
| FeedBackEndPoints | postUserFeedBack | POST | `/ngprofile/feedback/self` |
| FeedBackEndPoints | whatmaWebjobfeedback | POST | `/spapply/jobapplier/user/webjobfeedback` |
| InboxEndPoints | inboxListingApi | GET | `/ngjobseeker/inbox/mails/v2` |
| JobTabsEndPoint | fetchJobDetail | GET | `/spapi/jobs/` |
| JobTabsEndPoint | fetchSimilarJobs | GET | `/spapi/jobs/similar/` |
| JobTabsEndPoint | getBrowseJobsInBulk | POST | `/spapi/browsejobs/bulk` |
| JobTabsEndPoint | getCategoryJobsForDasBoard | POST | `/spapi/browsejobs/bulk` |
| JobTabsEndPoint | getJobsRecommendation | GET | `/spapi/jobapi/userjobrecommendations` |
| LoginEndPoint | appPullBlocker | GET | `/ngprofile/app/pullback` |
| LoginEndPoint | changeEmailApi | POST | `/nglogin/user/self/changeEmail` |
| LoginEndPoint | changePassword | POST | `/nglogin/user/self/changePassword` |
| LoginEndPoint | createPassword | POST | `/nglogin/user/self/setPassword` |
| LoginEndPoint | fetchEmailValidation | GET | `/ngprofile/user/emailValidation` |
| LoginEndPoint | forgetPwdLink | POST | `/nglogin/user/self/changePasswordFromLink` |
| LoginEndPoint | loginUserToServer | POST | `/nglogin/user/login` |
| LoginEndPoint | logoutUserToServer | POST | `/nglogin/user/logout` |
| LoginEndPoint | verifyResetPasswordLink | POST | `/nglogin/user/verifyResetPasswordLink` |
| NG360EndPoints | getPackagingDetailsForLoggedInUser | ? | `/ng360central/ng360Packaging/self/getDetails` |
| NG360EndPoints | getPackagingDetailsForLoggedOutUser | ? | `/ng360central/ng360Packaging/getLoggedOutLandingPage` |
| NGAssessmentEndPoints | getAssessmentListing | GET | `/ngassessment/users/self` |
| NGCQPrefillEndPoints | prefill | ? | `/spapply/genai/self/cq/prefill` |
| NGPageConfigEndPoints | getPageConfig | ? | `/spapi/pageConfig/v0` |
| NGPushdownEndPoints | getPushdownLayer | GET | `/ngprofile/v6/user/self/platform/dashboard/qup` |
| NGPushdownEndPoints | postPushdownFFLayerActionUpdate | POST | `/ngprofile/user/self/platform/\(platform)/optType/\(actionType)/ffLayer` |
| NGSearchWithAIEndPoints | extractNer | ? | `/spapi/jobapi/extractNer` |
| NGSearchWithAIUsageLimitEndPoints | checkUsageLimit | ? | `/spapi/jobapi/usage-limit/check` |
| NGSearchWithAIUsageLimitEndPoints | checkUsageLimitSilent | ? | `/spapi/jobapi/usage-limit/check` |
| OAuthEndPoints | portLogin | GET | `/ni/nilogin/user/AtFromConmnj` |
| ProfileEndPoints | deleteEducationType | POST | `/ngprofile/user/self/section/\(type.cleanString())` |
| ProfileEndPoints | fetchNewAISummaryToken | GET | `/ngprofile/user/self/generateNewAISummary` |
| ProfileEndPoints | generateNewAISummaryStream | GET | `/gen-ai/processor/template/stream` |
| ProfileEndPoints | getFullProfileApi | GET | `/ngprofile/aggregate/self/fullProfile` |
| ProfileEndPoints | getParticularSectionDataFromServer | GET | `/ngprofile/user/self` |
| ProfileEndPoints | getProfileDashBoardAggregator | GET | `/ngprofile/aggregate/self/dashboardData` |
| ProfileEndPoints | getVerificationType | GET | `/ngprofile/otp/self/verificationType` |
| ProfileEndPoints | sendOtpToMobileApi | GET | `/ngprofile/otp/self/sendOTP` |
| ProfileEndPoints | updateMultiPushDownData | POST | `/ngprofile/recQup/user/self/submitQupData` |
| ProfileEndPoints | updateProfileData | POST | `/ngprofile/user/self/section/` |
| ProfileEndPoints | updatePushdownData | POST | `/ngprofile/user/self/section/` |
| ProfileEndPoints | verifyOtpApi | POST | `/ngprofile/otp/self/verifyOTP` |
| ProfilePhotoEndPoints | deleteProfilePhotoFromServer | POST | `/ngprofile/user/self/section/photoAttachment` |
| ProfilePhotoEndPoints | getProfilePhotoFromServer | GET | `/ngprofile/user/self/photoAttachment/link` |
| ProfilePhotoEndPoints | uploadProfilePhotoOnServerSide | POST | `/file` |
| ProfilePhotoEndPoints | uploadProfilePhotoWithFileKey | POST | `/ngprofile/user/self/section/photoAttachment` |
| ProfileUploadCVEndPoints | deleteCVFromServer | POST | `/ngprofile/user/self/section/cvAttachment` |
| ProfileUploadCVEndPoints | downloadAttachment | GET | `/ngprofile/user/self\(params)` |
| ProfileUploadCVEndPoints | downloadCVFromServer | GET | `/ngprofile/user/self/cvAttachment` |
| ProfileUploadCVEndPoints | getCVMetaDataFromServer | GET | `/ngprofile/user/self` |
| ProfileUploadCVEndPoints | uploadAccompToServer | POST | `/ngprofile/user/self/section/` |
| ProfileUploadCVEndPoints | uploadAccomplishmetFileToServer | POST | `/orchestration/file` |
| ProfileUploadCVEndPoints | uploadCVToServer | POST | `/ngfilevalidation/file` |
| ProfileUploadCVEndPoints | uploadFileFormKeyToServer | POST | `/ngprofile/user/self/section/cvAttachment` |
| PushNotificationTokenEndPoint | deleteApnsTokenForLoggedInUser | ? | `/ngenrollment/v0/logout` |
| PushNotificationTokenEndPoint | saveDeviceTokenToServer | ? | `/ngenrollment/v0/registerDevice` |
| PushNotificationTokenEndPoint | updateApnsSettingAPI | ? | `/ngenrollment/v0/device/settings` |
| PushNotificationTokenEndPoint | updateApnsTokenForLoggedInUser | ? | `/ngenrollment/v0/registerDevice` |
| PushNotificationTokenEndPoint | updateDeviceTokenToServer | ? | `/ngenrollment/v0/updateDevice` |
| RegistrationApi | checkRegisteredEmail | GET | `/resman/user/register/checkEmail` |
| RegistrationApi | cvParser | POST | `/ngparser/cvParser` |
| RegistrationApi | getCompWithIndJson | GET | `/s/2/200/j/compWithIndAreaSugg.json` |
| RegistrationApi | getDesigWithFAreaJson | GET | `/s/2/200/j/desigWithFAreaSugg.json` |
| RegistrationApi | getIdFromServer | GET | `/ngresman/user/experiment/\(experimentType)` |
| RegistrationApi | registerUserToServer | POST | `/ngresman/user` |
| RegistrationApi | sendDataToServerWithAuth | POST | `/ngresman/user/experiment/\(experimentType)/page/` |
| RegistrationApi | sendDataToUnReg | POST | `/ngresman/user/unreg` |
| RegistrationApi | sendEmailVerificationOTP | POST | `/ngprofile/email/self/sendEmailVerificationOTP` |
| RegistrationApi | sendUploadCvReminder | POST | `/ngprofile/user/self/uploadCvReminder` |
| RegistrationApi | verifyEmailOTP | POST | `/ngprofile/email/self/verifyEmailOTP` |
| SearchJobEndPoint | getJobsFromSearchApi | GET | `/spapi/jobapi/search` |
| SearchJobEndPoint | getRecentSearchFromApi | GET | `/spapi/jobapi/recentsearch` |
| SearchJobEndPoint | getRedirectionCodeApi | GET | `/spapi/jobapi/redirectionCode` |
| SearchJobEndPoint | postAndGetRecentSearches | POST | `/spapi/jobapi/recentSearchJobCount` |
| SearchJobEndPoint | postRecentSearchDataCount | POST | `/spapi/jobapi/recentSearchJobCount` |
| SettingsEndPoint | deactivateUserProfile | POST | `/ngprofile/user/self/visibility` |
| SettingsEndPoint | deleteProfile | POST | `/ngprofile/user/self/deleteProfile` |
| SettingsEndPoint | fetchMailerSetting | GET | `/ngprofile/user/self/emailPreference` |
| SettingsEndPoint | fetchProfileVisibiltySetting | GET | `/ngprofile/user/self/visibility` |
| SettingsEndPoint | updateActiveOrPartialActiveProfile | POST | `/ngprofile/user/self/visibility` |
| SettingsEndPoint | updateMailerSetting | POST | `/ngprofile/user/self/emailPreference` |
| ShortlistedEndPoint | deleteShortlistJobs | POST | `/spapi/jobs/shortlist/` |
| ShortlistedEndPoint | getShortlistJobs | GET | `/spapi/jobs/shortlist` |
| ShortlistedEndPoint | saveBulkShortlistJobs | POST | `/spapi/jobs/shortlist` |
| ShortlistedEndPoint | updateShortlistJobs | POST | `/spapi/jobs/shortlist/` |
| SocialApiEndPoints | getSocialLoginDetails | GET | `/nglogin/user/self/socialLoginDetails` |
| SocialApiEndPoints | postConnectSocial | POST | `/nglogin/user/self/socialConnect` |
| SocialApiEndPoints | postDisconnectSocial | POST | `/nglogin/user/self/socialDisconnect` |
| SuggestorEndPoint | fetchACSuggestor | GET | `/suggest/ngCommonSuggester` |
| SuggestorEndPoint | fetchRCSuggestor | GET | `/suggest/ngRelatedConcepts` |
| SuggestorEndPoint | fetchTaxonomySuggestor | GET | `/suggest/taxonomyCommonSuggester` |
| WidgetSDKEndPoint | fetchV2WidgetData | ? | `/ims/page/pagename/\(name.cleanString())` |
| WidgetSDKEndPoint | viewAllCompanyBranding | ? | `/imsPage/ad/branding/viewAll` |
