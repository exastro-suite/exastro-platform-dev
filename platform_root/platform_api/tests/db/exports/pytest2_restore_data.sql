SET foreign_key_checks = 0;
DELETE FROM keycloak.databasechangelog;
DELETE FROM keycloak.idp_mapper_config;
DELETE FROM keycloak.databasechangeloglock;
DELETE FROM keycloak.realm_enabled_event_types;
DELETE FROM keycloak.client;
DELETE FROM keycloak.realm_smtp_config;
DELETE FROM keycloak.composite_role;
DELETE FROM keycloak.federated_user;
DELETE FROM keycloak.identity_provider_config;
DELETE FROM keycloak.event_entity;
DELETE FROM keycloak.resource_scope;
DELETE FROM keycloak.org;
DELETE FROM keycloak.identity_provider;
DELETE FROM keycloak.authenticator_config_entry;
DELETE FROM keycloak.redirect_uris;
DELETE FROM keycloak.scope_mapping;
DELETE FROM keycloak.component_config;
DELETE FROM keycloak.user_federation_provider;
DELETE FROM keycloak.group_attribute;
DELETE FROM keycloak.user_role_mapping;
DELETE FROM keycloak.realm_localizations;
DELETE FROM keycloak.outbox_entry;
DELETE FROM keycloak.fed_user_ver_credential;
DELETE FROM keycloak.web_origins;
DELETE FROM keycloak.user_federation_config;
DELETE FROM keycloak.revoked_token;
DELETE FROM keycloak.migration_model;
DELETE FROM keycloak.user_attribute;
DELETE FROM keycloak.keycloak_group;
DELETE FROM keycloak.server_config;
DELETE FROM keycloak.workflow_state;
DELETE FROM keycloak.org_invitation;
DELETE FROM keycloak.policy_config;
DELETE FROM keycloak.realm_attribute;
DELETE FROM keycloak.realm_events_listeners;
DELETE FROM keycloak.admin_event_entity;
DELETE FROM keycloak.user_entity;
DELETE FROM keycloak.broker_link;
DELETE FROM keycloak.client_auth_flow_bindings;
DELETE FROM keycloak.realm_required_credential;
DELETE FROM keycloak.resource_server_resource;
DELETE FROM keycloak.realm;
DELETE FROM keycloak.client_attributes;
DELETE FROM keycloak.jgroups_ping;
DELETE FROM keycloak.resource_server;
DELETE FROM keycloak.federated_identity;
DELETE FROM keycloak.realm_supported_locales;
DELETE FROM keycloak.login_failure;
DELETE FROM keycloak.protocol_mapper;
DELETE FROM keycloak.auth_session;
DELETE FROM keycloak.resource_uris;
DELETE FROM keycloak.client_initial_access;
DELETE FROM keycloak.identity_provider_mapper;
DELETE FROM keycloak.cluster_event;
DELETE FROM keycloak.resource_attribute;
DELETE FROM keycloak.user_ver_credential;
DELETE FROM keycloak.client_node_registrations;
DELETE FROM keycloak.client_scope_client;
DELETE FROM keycloak.fed_user_credential;
DELETE FROM keycloak.resource_server_policy;
DELETE FROM keycloak.fed_user_consent;
DELETE FROM keycloak.client_scope_role_mapping;
DELETE FROM keycloak.resource_server_scope;
DELETE FROM keycloak.scope_policy;
DELETE FROM keycloak.role_attribute;
DELETE FROM keycloak.associated_policy;
DELETE FROM keycloak.root_auth_session;
DELETE FROM keycloak.fed_user_group_membership;
DELETE FROM keycloak.offline_client_session;
DELETE FROM keycloak.keycloak_role;
DELETE FROM keycloak.user_required_action;
DELETE FROM keycloak.fed_user_role_mapping;
DELETE FROM keycloak.component;
DELETE FROM keycloak.issued_ver_credential;
DELETE FROM keycloak.authentication_flow;
DELETE FROM keycloak.authentication_execution;
DELETE FROM keycloak.user_federation_mapper;
DELETE FROM keycloak.user_federation_mapper_config;
DELETE FROM keycloak.protocol_mapper_config;
DELETE FROM keycloak.authenticator_config;
DELETE FROM keycloak.user_consent;
DELETE FROM keycloak.required_action_config;
DELETE FROM keycloak.required_action_provider;
DELETE FROM keycloak.user_consent_client_scope;
DELETE FROM keycloak.org_domain;
DELETE FROM keycloak.offline_user_session;
DELETE FROM keycloak.fed_user_consent_cl_scope;
DELETE FROM keycloak.fed_user_required_action;
DELETE FROM keycloak.user_group_membership;
DELETE FROM keycloak.group_role_mapping;
DELETE FROM keycloak.realm_default_groups;
DELETE FROM keycloak.credential;
DELETE FROM keycloak.client_scope;
DELETE FROM keycloak.resource_policy;
DELETE FROM keycloak.fed_user_attribute;
DELETE FROM keycloak.client_scope_attributes;
DELETE FROM keycloak.default_client_scope;
DELETE FROM keycloak.resource_server_perm_ticket;
DELETE FROM keycloak.fed_issued_ver_credential;
DELETE FROM keycloak.single_use_object;
DELETE FROM keycloak.org_identity_provider;
DELETE FROM platform.t_platform_version;
DELETE FROM platform.t_platform_migration_history;
DELETE FROM platform.t_platform_private;
DELETE FROM platform.t_organization;
DELETE FROM platform.t_organization_db;
DELETE FROM platform.t_organization_plan;
DELETE FROM platform.t_plan;
DELETE FROM platform.t_plan_item;
DELETE FROM platform.t_refresh_token;
DELETE FROM platform.m_system_config;
DELETE FROM platform.t_maintenance_mode;
DELETE FROM platform.t_process_queue;
DELETE FROM platform.t_plan_limit;
DELETE FROM platform.t_process_queue_lock;
-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: ita-mariadb    Database: keycloak
-- ------------------------------------------------------
-- Server version	5.5.5-10.11.4-MariaDB-1:10.11.4+maria~ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `keycloak`
--

USE `keycloak`;

--
-- Dumping data for table `admin_event_entity`
--

LOCK TABLES `admin_event_entity` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `associated_policy`
--

LOCK TABLES `associated_policy` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `auth_session`
--

LOCK TABLES `auth_session` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `authentication_execution`
--

LOCK TABLES `authentication_execution` WRITE;
INSERT INTO `authentication_execution` VALUES ('00e160ce-f862-4a3b-ad95-61bd7ab31492',NULL,'auth-recovery-authn-code-form','faaacb96-1668-4dd7-b538-000594f408e6','56b10386-29a9-46b4-a812-9c30a5d74545',3,50,0,NULL,NULL),('096ac852-aaf0-4e20-880d-68b7115115b9',NULL,'conditional-credential','faaacb96-1668-4dd7-b538-000594f408e6','56b10386-29a9-46b4-a812-9c30a5d74545',0,20,0,NULL,'ed47b689-9b92-4ae4-9db0-d94d50df352c'),('0a030669-d45e-4d13-b4c9-17a32f72c160',NULL,'idp-confirm-link','faaacb96-1668-4dd7-b538-000594f408e6','1811adae-34a4-4310-9beb-a810d19a5abe',0,10,0,NULL,NULL),('1749fbc4-b177-426b-a77a-473df4061743',NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','1f73705a-3eed-4433-9b87-68f9aa788717',2,30,1,'b8b27bba-daca-4193-84c3-1f6db87235ae',NULL),('17e2cee2-7cd6-4d6b-b810-03048aecf131',NULL,'reset-password','faaacb96-1668-4dd7-b538-000594f408e6','00614996-4f54-4c94-855d-18ba4c98ffc3',0,30,0,NULL,NULL),('182dcff5-2264-4ba1-93bf-f56f1e0b8990',NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','b8b27bba-daca-4193-84c3-1f6db87235ae',1,20,1,'d10c28ef-c967-4616-8cd4-a81079eaeeca',NULL),('1a144d93-dfd9-4569-b895-a4f4fb484eee',NULL,'conditional-user-configured','faaacb96-1668-4dd7-b538-000594f408e6','1a31dea8-5eba-4d7e-9d70-95f9b8a2ca04',0,10,0,NULL,NULL),('1ca37270-c69e-4eab-a84c-d4b77bffeea4',NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','1811adae-34a4-4310-9beb-a810d19a5abe',0,20,1,'7b510357-2e20-488a-8916-319d6091d68e',NULL),('24bfc0d2-bacf-4756-b767-1c7446a85a97',NULL,'webauthn-authenticator','faaacb96-1668-4dd7-b538-000594f408e6','d10c28ef-c967-4616-8cd4-a81079eaeeca',3,40,0,NULL,NULL),('28d84c28-48e9-401c-9813-5cb033a76725',NULL,'auth-spnego','faaacb96-1668-4dd7-b538-000594f408e6','1f73705a-3eed-4433-9b87-68f9aa788717',3,20,0,NULL,NULL),('29cf6a03-0d91-4697-a8f7-0fe2b1a1b166',NULL,'auth-cookie','faaacb96-1668-4dd7-b538-000594f408e6','1f73705a-3eed-4433-9b87-68f9aa788717',2,10,0,NULL,NULL),('2a234c2a-5c45-4d76-b252-f4e698d5bd3c',NULL,'registration-user-creation','faaacb96-1668-4dd7-b538-000594f408e6','596dd88e-b71f-48a0-a9c2-4f224aaf0023',0,20,0,NULL,NULL),('2b208865-2b54-4264-9663-2ab795f38521',NULL,'client-secret-jwt','faaacb96-1668-4dd7-b538-000594f408e6','cacb068a-38fa-454b-9b33-251c9a54669c',2,30,0,NULL,NULL),('2f6393ac-c4ec-4740-acfe-9ee27ba9915f',NULL,'conditional-user-configured','faaacb96-1668-4dd7-b538-000594f408e6','56b10386-29a9-46b4-a812-9c30a5d74545',0,10,0,NULL,NULL),('3f2c5c2e-73bd-44c0-82fd-982772ba3d6c',NULL,'auth-otp-form','faaacb96-1668-4dd7-b538-000594f408e6','d10c28ef-c967-4616-8cd4-a81079eaeeca',2,30,0,NULL,NULL),('43879a2a-ea3a-4068-8fe3-ab86e9d91975',NULL,'client-secret','faaacb96-1668-4dd7-b538-000594f408e6','cacb068a-38fa-454b-9b33-251c9a54669c',2,10,0,NULL,NULL),('4b0266c6-7592-40bd-93aa-aa0be7565993',NULL,'conditional-user-configured','faaacb96-1668-4dd7-b538-000594f408e6','effb2495-10e6-4ae1-b544-9bf4457efc3a',0,10,0,NULL,NULL),('4c5ca8d7-02e6-46f2-91a3-e87c76ec6251',NULL,'direct-grant-validate-password','faaacb96-1668-4dd7-b538-000594f408e6','f90efcf4-2095-41b5-abd1-93c4420436d4',0,20,0,NULL,NULL),('50e783bc-aef5-418b-9b69-fb2d365acb85',NULL,'federated-jwt','faaacb96-1668-4dd7-b538-000594f408e6','cacb068a-38fa-454b-9b33-251c9a54669c',2,50,0,NULL,NULL),('58fc63f5-40cf-4d17-bb52-dd0deb276617',NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','2b32921f-c16d-4224-8e9b-c1b9ed64b58d',0,20,1,'2294952b-fe5f-44cc-a847-fbff04602ad7',NULL),('598c7424-d12c-468c-b179-2f228b77209d',NULL,'idp-create-user-if-unique','faaacb96-1668-4dd7-b538-000594f408e6','2294952b-fe5f-44cc-a847-fbff04602ad7',2,10,0,NULL,'764e2d14-2acd-4fab-af11-46bfd812a70e'),('5dfa57bb-34c5-45d6-aa2d-43d652557574',NULL,'auth-recovery-authn-code-form','faaacb96-1668-4dd7-b538-000594f408e6','d10c28ef-c967-4616-8cd4-a81079eaeeca',3,50,0,NULL,NULL),('65a27b14-e080-42bb-9761-e48494957a52',NULL,'direct-grant-validate-username','faaacb96-1668-4dd7-b538-000594f408e6','f90efcf4-2095-41b5-abd1-93c4420436d4',0,10,0,NULL,NULL),('6853d7c3-5ebe-4f10-9a1c-d3050a4ac74e',NULL,'client-x509','faaacb96-1668-4dd7-b538-000594f408e6','cacb068a-38fa-454b-9b33-251c9a54669c',2,40,0,NULL,NULL),('73771d3e-d79a-418d-8eaf-38fd4ccdfbbe',NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','2294952b-fe5f-44cc-a847-fbff04602ad7',2,20,1,'1811adae-34a4-4310-9beb-a810d19a5abe',NULL),('793bd6fd-6fd2-4e9c-ac93-bf144cd50805',NULL,'client-jwt','faaacb96-1668-4dd7-b538-000594f408e6','cacb068a-38fa-454b-9b33-251c9a54669c',2,20,0,NULL,NULL),('79d2dff8-c459-4f54-8c6f-68b33612cfec',NULL,'docker-http-basic-authenticator','faaacb96-1668-4dd7-b538-000594f408e6','726ff5d4-3bde-4d80-b4d6-43b597c55e68',0,10,0,NULL,NULL),('7a40ddf0-7d80-41f1-8981-e4adcaffc598',NULL,'reset-credentials-choose-user','faaacb96-1668-4dd7-b538-000594f408e6','00614996-4f54-4c94-855d-18ba4c98ffc3',0,10,0,NULL,NULL),('86e86455-40ca-4a12-955d-19f3728add61',NULL,'idp-review-profile','faaacb96-1668-4dd7-b538-000594f408e6','2b32921f-c16d-4224-8e9b-c1b9ed64b58d',0,10,0,NULL,'775c9b2e-77a5-40a8-b151-4cad78d417b7'),('8efd2083-7765-460f-adc0-945b9b4dbe4c',NULL,'registration-terms-and-conditions','faaacb96-1668-4dd7-b538-000594f408e6','596dd88e-b71f-48a0-a9c2-4f224aaf0023',3,70,0,NULL,NULL),('91ca6f15-5187-4b77-b1b7-5e4322d6e7b5',NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','4a607cb8-41a7-4778-ac09-79a9e596587e',1,20,1,'56b10386-29a9-46b4-a812-9c30a5d74545',NULL),('937de136-0c52-45ee-8c0f-d43ab05fcf20',NULL,'auth-otp-form','faaacb96-1668-4dd7-b538-000594f408e6','56b10386-29a9-46b4-a812-9c30a5d74545',2,30,0,NULL,NULL),('939f95d4-e796-4434-bbbc-bac236c20900',NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','7b510357-2e20-488a-8916-319d6091d68e',2,20,1,'4a607cb8-41a7-4778-ac09-79a9e596587e',NULL),('93c25191-6556-4ef5-89ef-6a55698d0e2c',NULL,'idp-username-password-form','faaacb96-1668-4dd7-b538-000594f408e6','4a607cb8-41a7-4778-ac09-79a9e596587e',0,10,0,NULL,NULL),('94b1d875-22d5-44e2-bced-81fb3165b44d',NULL,'conditional-credential','faaacb96-1668-4dd7-b538-000594f408e6','d10c28ef-c967-4616-8cd4-a81079eaeeca',0,20,0,NULL,'54e17ac6-117a-4863-80a2-3560017b54ff'),('a95e611b-e765-4b46-bbf1-6a4c327c9ff6',NULL,'registration-password-action','faaacb96-1668-4dd7-b538-000594f408e6','596dd88e-b71f-48a0-a9c2-4f224aaf0023',0,50,0,NULL,NULL),('acbd1d1e-5d15-4248-90bb-1ec18256919b',NULL,'reset-otp','faaacb96-1668-4dd7-b538-000594f408e6','effb2495-10e6-4ae1-b544-9bf4457efc3a',0,20,0,NULL,NULL),('b423f4c3-0e09-4b23-99d1-1c18f919ac63',NULL,'identity-provider-redirector','faaacb96-1668-4dd7-b538-000594f408e6','1f73705a-3eed-4433-9b87-68f9aa788717',2,25,0,NULL,NULL),('b93078f0-4ee7-4e2c-9b98-551dda719249',NULL,'idp-email-verification','faaacb96-1668-4dd7-b538-000594f408e6','7b510357-2e20-488a-8916-319d6091d68e',2,10,0,NULL,NULL),('b96c28fe-0e3b-4994-a98e-67191d2a2ce1',NULL,'direct-grant-validate-otp','faaacb96-1668-4dd7-b538-000594f408e6','1a31dea8-5eba-4d7e-9d70-95f9b8a2ca04',0,20,0,NULL,NULL),('c06468ee-2b09-45ad-bfc0-93e90fcfe366',NULL,'conditional-user-configured','faaacb96-1668-4dd7-b538-000594f408e6','d10c28ef-c967-4616-8cd4-a81079eaeeca',0,10,0,NULL,NULL),('c4bfe745-4173-4e85-afd1-fc0178d4e4aa',NULL,'http-basic-authenticator','faaacb96-1668-4dd7-b538-000594f408e6','b891def6-5f78-47f9-ad27-165bbce15d58',0,10,0,NULL,NULL),('c8152b2f-0e11-402c-bd6c-028304cbdf1c',NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','f90efcf4-2095-41b5-abd1-93c4420436d4',1,30,1,'1a31dea8-5eba-4d7e-9d70-95f9b8a2ca04',NULL),('d6052478-b765-4168-9722-de4715d4d7ad',NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','00614996-4f54-4c94-855d-18ba4c98ffc3',1,40,1,'effb2495-10e6-4ae1-b544-9bf4457efc3a',NULL),('d6b9858e-d5be-4df1-a7c8-8fd29573e940',NULL,'reset-credential-email','faaacb96-1668-4dd7-b538-000594f408e6','00614996-4f54-4c94-855d-18ba4c98ffc3',0,20,0,NULL,NULL),('db0a2359-20e9-4c12-9cb3-2b78ff38caf8',NULL,'auth-username-password-form','faaacb96-1668-4dd7-b538-000594f408e6','b8b27bba-daca-4193-84c3-1f6db87235ae',0,10,0,NULL,NULL),('f0625398-a5b1-4b87-848f-ac79aeeb2dde',NULL,'registration-page-form','faaacb96-1668-4dd7-b538-000594f408e6','7b08e83a-e376-42ff-8b86-e8cf756691a0',0,10,1,'596dd88e-b71f-48a0-a9c2-4f224aaf0023',NULL),('f37e5ea0-8771-45ff-bafa-7eb582cdd5da',NULL,'webauthn-authenticator','faaacb96-1668-4dd7-b538-000594f408e6','56b10386-29a9-46b4-a812-9c30a5d74545',3,40,0,NULL,NULL),('fef67066-aac5-42af-a350-6637dd4f7641',NULL,'registration-recaptcha-action','faaacb96-1668-4dd7-b538-000594f408e6','596dd88e-b71f-48a0-a9c2-4f224aaf0023',3,60,0,NULL,NULL);
UNLOCK TABLES;

--
-- Dumping data for table `authentication_flow`
--

LOCK TABLES `authentication_flow` WRITE;
INSERT INTO `authentication_flow` VALUES ('00614996-4f54-4c94-855d-18ba4c98ffc3','reset credentials','Reset credentials for a user if they forgot their password or something','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',1,1),('1811adae-34a4-4310-9beb-a810d19a5abe','Handle Existing Account','Handle what to do if there is existing account with same email/username like authenticated identity provider','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',0,1),('1a31dea8-5eba-4d7e-9d70-95f9b8a2ca04','Direct Grant - Conditional OTP','Flow to determine if the OTP is required for the authentication','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',0,1),('1f73705a-3eed-4433-9b87-68f9aa788717','browser','Browser based authentication','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',1,1),('2294952b-fe5f-44cc-a847-fbff04602ad7','User creation or linking','Flow for the existing/non-existing user alternatives','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',0,1),('2b32921f-c16d-4224-8e9b-c1b9ed64b58d','first broker login','Actions taken after first broker login with identity provider account, which is not yet linked to any Keycloak account','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',1,1),('4a607cb8-41a7-4778-ac09-79a9e596587e','Verify Existing Account by Re-authentication','Reauthentication of existing account','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',0,1),('56b10386-29a9-46b4-a812-9c30a5d74545','First broker login - Conditional 2FA','Flow to determine if any 2FA is required for the authentication','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',0,1),('596dd88e-b71f-48a0-a9c2-4f224aaf0023','registration form','Registration form','faaacb96-1668-4dd7-b538-000594f408e6','form-flow',0,1),('726ff5d4-3bde-4d80-b4d6-43b597c55e68','docker auth','Used by Docker clients to authenticate against the IDP','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',1,1),('7b08e83a-e376-42ff-8b86-e8cf756691a0','registration','Registration flow','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',1,1),('7b510357-2e20-488a-8916-319d6091d68e','Account verification options','Method with which to verify the existing account','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',0,1),('b891def6-5f78-47f9-ad27-165bbce15d58','saml ecp','SAML ECP Profile Authentication Flow','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',1,1),('b8b27bba-daca-4193-84c3-1f6db87235ae','forms','Username, password, otp and other auth forms.','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',0,1),('cacb068a-38fa-454b-9b33-251c9a54669c','clients','Base authentication for clients','faaacb96-1668-4dd7-b538-000594f408e6','client-flow',1,1),('d10c28ef-c967-4616-8cd4-a81079eaeeca','Browser - Conditional 2FA','Flow to determine if any 2FA is required for the authentication','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',0,1),('effb2495-10e6-4ae1-b544-9bf4457efc3a','Reset - Conditional OTP','Flow to determine if the OTP should be reset or not. Set to REQUIRED to force.','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',0,1),('f90efcf4-2095-41b5-abd1-93c4420436d4','direct grant','OpenID Connect Resource Owner Grant','faaacb96-1668-4dd7-b538-000594f408e6','basic-flow',1,1);
UNLOCK TABLES;

--
-- Dumping data for table `authenticator_config`
--

LOCK TABLES `authenticator_config` WRITE;
INSERT INTO `authenticator_config` VALUES ('54e17ac6-117a-4863-80a2-3560017b54ff','browser-conditional-credential','faaacb96-1668-4dd7-b538-000594f408e6'),('764e2d14-2acd-4fab-af11-46bfd812a70e','create unique user config','faaacb96-1668-4dd7-b538-000594f408e6'),('775c9b2e-77a5-40a8-b151-4cad78d417b7','review profile config','faaacb96-1668-4dd7-b538-000594f408e6'),('ed47b689-9b92-4ae4-9db0-d94d50df352c','first-broker-login-conditional-credential','faaacb96-1668-4dd7-b538-000594f408e6');
UNLOCK TABLES;

--
-- Dumping data for table `authenticator_config_entry`
--

LOCK TABLES `authenticator_config_entry` WRITE;
INSERT INTO `authenticator_config_entry` VALUES ('54e17ac6-117a-4863-80a2-3560017b54ff','webauthn-passwordless','credentials'),('764e2d14-2acd-4fab-af11-46bfd812a70e','false','require.password.update.after.registration'),('775c9b2e-77a5-40a8-b151-4cad78d417b7','missing','update.profile.on.first.login'),('ed47b689-9b92-4ae4-9db0-d94d50df352c','webauthn-passwordless','credentials');
UNLOCK TABLES;

--
-- Dumping data for table `broker_link`
--

LOCK TABLES `broker_link` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
INSERT INTO `client` VALUES ('0060978e-25c0-4f54-9b7b-74dbd36df936',1,1,'_platform',0,0,'ssTLKTLyDdb3kNve6TdbshIPLQnkjIQs7xP6nY218x9pSQDT23zOEH3y328Z1bhGptBmhgBdDwdlO0p6iSPU6D',NULL,0,NULL,0,'faaacb96-1668-4dd7-b538-000594f408e6','openid-connect',-1,0,0,NULL,1,'client-secret',NULL,NULL,NULL,0,0,1,0,1794211604305,1794211604371),('05d101c8-6190-4dbc-9613-97d8d570f470',1,1,'admin-cli',0,1,NULL,NULL,0,NULL,0,'faaacb96-1668-4dd7-b538-000594f408e6','openid-connect',0,0,0,'${client_admin-cli}',0,'client-secret',NULL,NULL,NULL,0,0,1,0,1794211595425,1794211595454),('262407fa-fb61-433e-bf95-a730e7df9247',1,0,'broker',0,0,NULL,NULL,1,NULL,0,'faaacb96-1668-4dd7-b538-000594f408e6','openid-connect',0,0,0,'${client_broker}',0,'client-secret',NULL,NULL,NULL,1,0,0,0,1794211595345,1794211595370),('4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,0,'master-realm',0,0,NULL,NULL,1,NULL,0,'faaacb96-1668-4dd7-b538-000594f408e6',NULL,0,0,0,'master Realm',0,'client-secret',NULL,NULL,NULL,1,0,0,0,1794211594981,1794211594986),('54c52862-bb56-483f-85dd-e529c984b618',1,1,'_platform-api',0,1,NULL,NULL,0,NULL,0,'faaacb96-1668-4dd7-b538-000594f408e6','openid-connect',-1,0,0,NULL,0,'client-secret',NULL,NULL,NULL,0,0,1,0,1794211604559,1794211604583),('7085a323-1455-4f1b-97f7-bfe1ffa52de8',1,1,'security-admin-console',0,1,NULL,'/admin/master/console/',0,NULL,0,'faaacb96-1668-4dd7-b538-000594f408e6','openid-connect',0,0,0,'${client_security-admin-console}',0,'client-secret','${authAdminUrl}',NULL,NULL,1,0,0,0,1794211595382,1794211595408),('7d911892-0def-4068-9047-457bdb014ab8',1,0,'_platform-console',0,1,'kpalic7ntro5FVRd6of9fBqpX7j6ZO2oWFhG0f50BtFd2DuXD5iiZty368iEs9NaAY7HtLEdY07RWkzNloPyIW',NULL,0,NULL,0,'faaacb96-1668-4dd7-b538-000594f408e6','openid-connect',-1,0,0,NULL,0,'client-secret',NULL,NULL,NULL,1,0,1,0,1794211605235,1794211605366),('8c6458b8-7b08-46db-bcfd-f98c4a29714b',1,0,'account-console',0,1,NULL,'/realms/master/account/',0,NULL,0,'faaacb96-1668-4dd7-b538-000594f408e6','openid-connect',0,0,0,'${client_account-console}',0,'client-secret','${authBaseUrl}',NULL,NULL,1,0,0,0,1794211595305,1794211595324),('c545dfde-c13c-40eb-bb45-72155bfcb98e',1,0,'account',0,1,NULL,'/realms/master/account/',0,NULL,0,'faaacb96-1668-4dd7-b538-000594f408e6','openid-connect',0,0,0,'${client_account}',0,'client-secret','${authBaseUrl}',NULL,NULL,1,0,0,0,1794211595205,1794211595236);
UNLOCK TABLES;

--
-- Dumping data for table `client_attributes`
--

LOCK TABLES `client_attributes` WRITE;
INSERT INTO `client_attributes` VALUES ('0060978e-25c0-4f54-9b7b-74dbd36df936','backchannel.logout.revoke.offline.tokens','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','backchannel.logout.session.required','true'),('0060978e-25c0-4f54-9b7b-74dbd36df936','client_credentials.use_refresh_token','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','client.secret.creation.time','1794211604'),('0060978e-25c0-4f54-9b7b-74dbd36df936','display.on.consent.screen','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','exclude.session.state.from.auth.response','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','id.token.as.detached.signature','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','oauth2.device.authorization.grant.enabled','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','oidc.ciba.grant.enabled','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','require.pushed.authorization.requests','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml_force_name_id_format','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.artifact.binding','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.assertion.signature','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.authnstatement','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.client.signature','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.encrypt','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.force.post.binding','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.multivalued.roles','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.onetimeuse.condition','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.server.signature','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','saml.server.signature.keyinfo.ext','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','tls.client.certificate.bound.access.tokens','false'),('0060978e-25c0-4f54-9b7b-74dbd36df936','use.refresh.tokens','true'),('05d101c8-6190-4dbc-9613-97d8d570f470','client.use.lightweight.access.token.enabled','true'),('54c52862-bb56-483f-85dd-e529c984b618','access.token.lifespan','86400'),('54c52862-bb56-483f-85dd-e529c984b618','acr.loa.map','{}'),('54c52862-bb56-483f-85dd-e529c984b618','backchannel.logout.revoke.offline.tokens','false'),('54c52862-bb56-483f-85dd-e529c984b618','backchannel.logout.session.required','true'),('54c52862-bb56-483f-85dd-e529c984b618','client_credentials.use_refresh_token','false'),('54c52862-bb56-483f-85dd-e529c984b618','client.session.idle.timeout','86400'),('54c52862-bb56-483f-85dd-e529c984b618','client.session.max.lifespan','86400'),('54c52862-bb56-483f-85dd-e529c984b618','display.on.consent.screen','false'),('54c52862-bb56-483f-85dd-e529c984b618','exclude.session.state.from.auth.response','false'),('54c52862-bb56-483f-85dd-e529c984b618','frontchannel.logout.session.required','false'),('54c52862-bb56-483f-85dd-e529c984b618','id.token.as.detached.signature','false'),('54c52862-bb56-483f-85dd-e529c984b618','oauth2.device.authorization.grant.enabled','false'),('54c52862-bb56-483f-85dd-e529c984b618','oidc.ciba.grant.enabled','false'),('54c52862-bb56-483f-85dd-e529c984b618','require.pushed.authorization.requests','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml_force_name_id_format','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.allow.ecp.flow','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.artifact.binding','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.assertion.signature','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.authnstatement','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.client.signature','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.encrypt','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.force.post.binding','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.multivalued.roles','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.onetimeuse.condition','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.server.signature','false'),('54c52862-bb56-483f-85dd-e529c984b618','saml.server.signature.keyinfo.ext','false'),('54c52862-bb56-483f-85dd-e529c984b618','tls.client.certificate.bound.access.tokens','false'),('54c52862-bb56-483f-85dd-e529c984b618','token.response.type.bearer.lower-case','false'),('54c52862-bb56-483f-85dd-e529c984b618','use.refresh.tokens','true'),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','client.use.lightweight.access.token.enabled','true'),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','pkce.code.challenge.method','S256'),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','post.logout.redirect.uris','+'),('7d911892-0def-4068-9047-457bdb014ab8','backchannel.logout.revoke.offline.tokens','false'),('7d911892-0def-4068-9047-457bdb014ab8','backchannel.logout.session.required','true'),('7d911892-0def-4068-9047-457bdb014ab8','client_credentials.use_refresh_token','false'),('7d911892-0def-4068-9047-457bdb014ab8','client.secret.creation.time','1794211605'),('7d911892-0def-4068-9047-457bdb014ab8','display.on.consent.screen','false'),('7d911892-0def-4068-9047-457bdb014ab8','exclude.session.state.from.auth.response','false'),('7d911892-0def-4068-9047-457bdb014ab8','id.token.as.detached.signature','false'),('7d911892-0def-4068-9047-457bdb014ab8','oauth2.device.authorization.grant.enabled','false'),('7d911892-0def-4068-9047-457bdb014ab8','oidc.ciba.grant.enabled','false'),('7d911892-0def-4068-9047-457bdb014ab8','post.logout.redirect.uris','/*'),('7d911892-0def-4068-9047-457bdb014ab8','require.pushed.authorization.requests','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml_force_name_id_format','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.artifact.binding','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.assertion.signature','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.authnstatement','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.client.signature','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.encrypt','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.force.post.binding','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.multivalued.roles','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.onetimeuse.condition','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.server.signature','false'),('7d911892-0def-4068-9047-457bdb014ab8','saml.server.signature.keyinfo.ext','false'),('7d911892-0def-4068-9047-457bdb014ab8','tls.client.certificate.bound.access.tokens','false'),('7d911892-0def-4068-9047-457bdb014ab8','use.refresh.tokens','true'),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','pkce.code.challenge.method','S256'),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','post.logout.redirect.uris','+'),('c545dfde-c13c-40eb-bb45-72155bfcb98e','post.logout.redirect.uris','+');
UNLOCK TABLES;

--
-- Dumping data for table `client_auth_flow_bindings`
--

LOCK TABLES `client_auth_flow_bindings` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `client_initial_access`
--

LOCK TABLES `client_initial_access` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `client_node_registrations`
--

LOCK TABLES `client_node_registrations` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `client_scope`
--

LOCK TABLES `client_scope` WRITE;
INSERT INTO `client_scope` VALUES ('0b5b5753-25ad-41c5-b2fb-024f036c101a','AuthnContextClassRef','faaacb96-1668-4dd7-b538-000594f408e6','AuthnContextClassRef Level of Authentiation','saml'),('1fdb82c7-6ab9-4d1f-b608-bd2f525fe810','email','faaacb96-1668-4dd7-b538-000594f408e6','OpenID Connect built-in scope: email','openid-connect'),('23dd2041-cb93-488c-9ef0-910909a90987','profile','faaacb96-1668-4dd7-b538-000594f408e6','OpenID Connect built-in scope: profile','openid-connect'),('2bbe7b9a-bdc7-4fff-94e6-bdc3584856da','service_account','faaacb96-1668-4dd7-b538-000594f408e6','Specific scope for a client enabled for service accounts','openid-connect'),('30671452-f0df-40bc-90c9-91222fc2bec5','offline_access','faaacb96-1668-4dd7-b538-000594f408e6','OpenID Connect built-in scope: offline_access','openid-connect'),('349cd61f-65a1-4f1e-9370-de157d8a9920','roles','faaacb96-1668-4dd7-b538-000594f408e6','OpenID Connect scope for add user roles to the access token','openid-connect'),('3ca64165-0619-47c2-9793-470f444c40c2','kc-admin-api','faaacb96-1668-4dd7-b538-000594f408e6','Grants access to the Keycloak Admin REST API by adding its required audience to the token','openid-connect'),('42d1ea7a-f39d-49c8-8777-7fd6b457e871','basic','faaacb96-1668-4dd7-b538-000594f408e6','OpenID Connect scope for add all basic claims to the token','openid-connect'),('4acbebfd-4e12-4551-afc9-6ea3682610a3','phone','faaacb96-1668-4dd7-b538-000594f408e6','OpenID Connect built-in scope: phone','openid-connect'),('5ac886e2-fbb9-44b5-9ff9-dbe4fa973d3f','saml_organization','faaacb96-1668-4dd7-b538-000594f408e6','Organization Membership','saml'),('5f5b905a-4d28-40f1-8350-99dfd37c904e','microprofile-jwt','faaacb96-1668-4dd7-b538-000594f408e6','Microprofile - JWT built-in scope','openid-connect'),('61f99739-6fce-43f9-958e-f3ea982b6e55','role_list','faaacb96-1668-4dd7-b538-000594f408e6','SAML role list','saml'),('67d5f582-ecc0-42d6-9f65-2c0452d5e397','web-origins','faaacb96-1668-4dd7-b538-000594f408e6','OpenID Connect scope for add allowed web origins to the access token','openid-connect'),('9be0037a-51a5-4eb3-b14a-24d9135ffd1c','address','faaacb96-1668-4dd7-b538-000594f408e6','OpenID Connect built-in scope: address','openid-connect'),('9e94b502-44b3-473d-a357-97ac8014913a','organization','faaacb96-1668-4dd7-b538-000594f408e6','Additional claims about the organization a subject belongs to','openid-connect'),('d14d6d0a-565b-48d1-b7d1-de0a879d723a','acr','faaacb96-1668-4dd7-b538-000594f408e6','OpenID Connect scope for add acr (authentication context class reference) to the token','openid-connect');
UNLOCK TABLES;

--
-- Dumping data for table `client_scope_attributes`
--

LOCK TABLES `client_scope_attributes` WRITE;
INSERT INTO `client_scope_attributes` VALUES ('1fdb82c7-6ab9-4d1f-b608-bd2f525fe810','${emailScopeConsentText}','consent.screen.text'),('1fdb82c7-6ab9-4d1f-b608-bd2f525fe810','true','display.on.consent.screen'),('1fdb82c7-6ab9-4d1f-b608-bd2f525fe810','true','include.in.token.scope'),('23dd2041-cb93-488c-9ef0-910909a90987','${profileScopeConsentText}','consent.screen.text'),('23dd2041-cb93-488c-9ef0-910909a90987','true','display.on.consent.screen'),('23dd2041-cb93-488c-9ef0-910909a90987','true','include.in.token.scope'),('2bbe7b9a-bdc7-4fff-94e6-bdc3584856da','false','display.on.consent.screen'),('2bbe7b9a-bdc7-4fff-94e6-bdc3584856da','false','include.in.token.scope'),('30671452-f0df-40bc-90c9-91222fc2bec5','${offlineAccessScopeConsentText}','consent.screen.text'),('30671452-f0df-40bc-90c9-91222fc2bec5','true','display.on.consent.screen'),('349cd61f-65a1-4f1e-9370-de157d8a9920','${rolesScopeConsentText}','consent.screen.text'),('349cd61f-65a1-4f1e-9370-de157d8a9920','true','display.on.consent.screen'),('349cd61f-65a1-4f1e-9370-de157d8a9920','false','include.in.token.scope'),('3ca64165-0619-47c2-9793-470f444c40c2','false','display.on.consent.screen'),('3ca64165-0619-47c2-9793-470f444c40c2','true','include.in.token.scope'),('42d1ea7a-f39d-49c8-8777-7fd6b457e871','false','display.on.consent.screen'),('42d1ea7a-f39d-49c8-8777-7fd6b457e871','false','include.in.token.scope'),('4acbebfd-4e12-4551-afc9-6ea3682610a3','${phoneScopeConsentText}','consent.screen.text'),('4acbebfd-4e12-4551-afc9-6ea3682610a3','true','display.on.consent.screen'),('4acbebfd-4e12-4551-afc9-6ea3682610a3','true','include.in.token.scope'),('5ac886e2-fbb9-44b5-9ff9-dbe4fa973d3f','false','display.on.consent.screen'),('5f5b905a-4d28-40f1-8350-99dfd37c904e','false','display.on.consent.screen'),('5f5b905a-4d28-40f1-8350-99dfd37c904e','true','include.in.token.scope'),('61f99739-6fce-43f9-958e-f3ea982b6e55','${samlRoleListScopeConsentText}','consent.screen.text'),('61f99739-6fce-43f9-958e-f3ea982b6e55','true','display.on.consent.screen'),('67d5f582-ecc0-42d6-9f65-2c0452d5e397','false','display.on.consent.screen'),('67d5f582-ecc0-42d6-9f65-2c0452d5e397','false','include.in.token.scope'),('9be0037a-51a5-4eb3-b14a-24d9135ffd1c','${addressScopeConsentText}','consent.screen.text'),('9be0037a-51a5-4eb3-b14a-24d9135ffd1c','true','display.on.consent.screen'),('9be0037a-51a5-4eb3-b14a-24d9135ffd1c','true','include.in.token.scope'),('9e94b502-44b3-473d-a357-97ac8014913a','${organizationScopeConsentText}','consent.screen.text'),('9e94b502-44b3-473d-a357-97ac8014913a','true','display.on.consent.screen'),('9e94b502-44b3-473d-a357-97ac8014913a','true','include.in.token.scope'),('d14d6d0a-565b-48d1-b7d1-de0a879d723a','false','display.on.consent.screen'),('d14d6d0a-565b-48d1-b7d1-de0a879d723a','false','include.in.token.scope');
UNLOCK TABLES;

--
-- Dumping data for table `client_scope_client`
--

LOCK TABLES `client_scope_client` WRITE;
INSERT INTO `client_scope_client` VALUES ('0060978e-25c0-4f54-9b7b-74dbd36df936','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('0060978e-25c0-4f54-9b7b-74dbd36df936','23dd2041-cb93-488c-9ef0-910909a90987',1),('0060978e-25c0-4f54-9b7b-74dbd36df936','2bbe7b9a-bdc7-4fff-94e6-bdc3584856da',1),('0060978e-25c0-4f54-9b7b-74dbd36df936','30671452-f0df-40bc-90c9-91222fc2bec5',0),('0060978e-25c0-4f54-9b7b-74dbd36df936','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('0060978e-25c0-4f54-9b7b-74dbd36df936','3ca64165-0619-47c2-9793-470f444c40c2',1),('0060978e-25c0-4f54-9b7b-74dbd36df936','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('0060978e-25c0-4f54-9b7b-74dbd36df936','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('0060978e-25c0-4f54-9b7b-74dbd36df936','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('0060978e-25c0-4f54-9b7b-74dbd36df936','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('0060978e-25c0-4f54-9b7b-74dbd36df936','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('05d101c8-6190-4dbc-9613-97d8d570f470','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('05d101c8-6190-4dbc-9613-97d8d570f470','23dd2041-cb93-488c-9ef0-910909a90987',1),('05d101c8-6190-4dbc-9613-97d8d570f470','30671452-f0df-40bc-90c9-91222fc2bec5',0),('05d101c8-6190-4dbc-9613-97d8d570f470','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('05d101c8-6190-4dbc-9613-97d8d570f470','3ca64165-0619-47c2-9793-470f444c40c2',1),('05d101c8-6190-4dbc-9613-97d8d570f470','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('05d101c8-6190-4dbc-9613-97d8d570f470','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('05d101c8-6190-4dbc-9613-97d8d570f470','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('05d101c8-6190-4dbc-9613-97d8d570f470','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('05d101c8-6190-4dbc-9613-97d8d570f470','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('05d101c8-6190-4dbc-9613-97d8d570f470','9e94b502-44b3-473d-a357-97ac8014913a',0),('05d101c8-6190-4dbc-9613-97d8d570f470','d14d6d0a-565b-48d1-b7d1-de0a879d723a',1),('262407fa-fb61-433e-bf95-a730e7df9247','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('262407fa-fb61-433e-bf95-a730e7df9247','23dd2041-cb93-488c-9ef0-910909a90987',1),('262407fa-fb61-433e-bf95-a730e7df9247','30671452-f0df-40bc-90c9-91222fc2bec5',0),('262407fa-fb61-433e-bf95-a730e7df9247','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('262407fa-fb61-433e-bf95-a730e7df9247','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('262407fa-fb61-433e-bf95-a730e7df9247','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('262407fa-fb61-433e-bf95-a730e7df9247','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('262407fa-fb61-433e-bf95-a730e7df9247','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('262407fa-fb61-433e-bf95-a730e7df9247','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('262407fa-fb61-433e-bf95-a730e7df9247','9e94b502-44b3-473d-a357-97ac8014913a',0),('262407fa-fb61-433e-bf95-a730e7df9247','d14d6d0a-565b-48d1-b7d1-de0a879d723a',1),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','23dd2041-cb93-488c-9ef0-910909a90987',1),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','30671452-f0df-40bc-90c9-91222fc2bec5',0),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','9e94b502-44b3-473d-a357-97ac8014913a',0),('4573d9bb-a896-4da1-b70a-a364fdaee9a6','d14d6d0a-565b-48d1-b7d1-de0a879d723a',1),('54c52862-bb56-483f-85dd-e529c984b618','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('54c52862-bb56-483f-85dd-e529c984b618','23dd2041-cb93-488c-9ef0-910909a90987',1),('54c52862-bb56-483f-85dd-e529c984b618','30671452-f0df-40bc-90c9-91222fc2bec5',0),('54c52862-bb56-483f-85dd-e529c984b618','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('54c52862-bb56-483f-85dd-e529c984b618','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('54c52862-bb56-483f-85dd-e529c984b618','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('54c52862-bb56-483f-85dd-e529c984b618','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('54c52862-bb56-483f-85dd-e529c984b618','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('54c52862-bb56-483f-85dd-e529c984b618','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('54c52862-bb56-483f-85dd-e529c984b618','d14d6d0a-565b-48d1-b7d1-de0a879d723a',1),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','23dd2041-cb93-488c-9ef0-910909a90987',1),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','30671452-f0df-40bc-90c9-91222fc2bec5',0),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','3ca64165-0619-47c2-9793-470f444c40c2',1),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','9e94b502-44b3-473d-a357-97ac8014913a',0),('7085a323-1455-4f1b-97f7-bfe1ffa52de8','d14d6d0a-565b-48d1-b7d1-de0a879d723a',1),('7d911892-0def-4068-9047-457bdb014ab8','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('7d911892-0def-4068-9047-457bdb014ab8','23dd2041-cb93-488c-9ef0-910909a90987',1),('7d911892-0def-4068-9047-457bdb014ab8','30671452-f0df-40bc-90c9-91222fc2bec5',0),('7d911892-0def-4068-9047-457bdb014ab8','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('7d911892-0def-4068-9047-457bdb014ab8','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('7d911892-0def-4068-9047-457bdb014ab8','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('7d911892-0def-4068-9047-457bdb014ab8','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('7d911892-0def-4068-9047-457bdb014ab8','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('7d911892-0def-4068-9047-457bdb014ab8','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','23dd2041-cb93-488c-9ef0-910909a90987',1),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','30671452-f0df-40bc-90c9-91222fc2bec5',0),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','9e94b502-44b3-473d-a357-97ac8014913a',0),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','d14d6d0a-565b-48d1-b7d1-de0a879d723a',1),('c545dfde-c13c-40eb-bb45-72155bfcb98e','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('c545dfde-c13c-40eb-bb45-72155bfcb98e','23dd2041-cb93-488c-9ef0-910909a90987',1),('c545dfde-c13c-40eb-bb45-72155bfcb98e','30671452-f0df-40bc-90c9-91222fc2bec5',0),('c545dfde-c13c-40eb-bb45-72155bfcb98e','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('c545dfde-c13c-40eb-bb45-72155bfcb98e','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('c545dfde-c13c-40eb-bb45-72155bfcb98e','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('c545dfde-c13c-40eb-bb45-72155bfcb98e','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('c545dfde-c13c-40eb-bb45-72155bfcb98e','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('c545dfde-c13c-40eb-bb45-72155bfcb98e','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('c545dfde-c13c-40eb-bb45-72155bfcb98e','9e94b502-44b3-473d-a357-97ac8014913a',0),('c545dfde-c13c-40eb-bb45-72155bfcb98e','d14d6d0a-565b-48d1-b7d1-de0a879d723a',1);
UNLOCK TABLES;

--
-- Dumping data for table `client_scope_role_mapping`
--

LOCK TABLES `client_scope_role_mapping` WRITE;
INSERT INTO `client_scope_role_mapping` VALUES ('30671452-f0df-40bc-90c9-91222fc2bec5','455d5e7c-72c5-4557-9544-ebcfe8e9a234');
UNLOCK TABLES;

--
-- Dumping data for table `cluster_event`
--

LOCK TABLES `cluster_event` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `component`
--

LOCK TABLES `component` WRITE;
INSERT INTO `component` VALUES ('135dd8bf-8022-40d8-8ac9-5d6a5040aa5c','hmac-generated-hs512','faaacb96-1668-4dd7-b538-000594f408e6','hmac-generated','org.keycloak.keys.KeyProvider','faaacb96-1668-4dd7-b538-000594f408e6',NULL),('24d95846-022e-4695-9878-7d64acfbe281','Full Scope Disabled','faaacb96-1668-4dd7-b538-000594f408e6','scope','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','authenticated'),('3dd53db3-b042-45ee-984f-c53c8f72f1e4','Allowed Protocol Mapper Types','faaacb96-1668-4dd7-b538-000594f408e6','allowed-protocol-mappers','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','anonymous'),('43873a4f-24c5-48d3-9d43-b16e18ac2b6b','Allowed Registration Web Origins','faaacb96-1668-4dd7-b538-000594f408e6','registration-web-origins','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','authenticated'),('52bdcc5a-3b26-4afd-9e4f-33e892bbb045','Full Scope Disabled','faaacb96-1668-4dd7-b538-000594f408e6','scope','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','anonymous'),('6ba2be1a-f0bc-445e-b8c6-21aa9f7ce9eb','Allowed Client Scopes','faaacb96-1668-4dd7-b538-000594f408e6','allowed-client-templates','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','anonymous'),('6e952c36-8dd0-4db2-9173-47f075f0cf5e','rsa-generated','faaacb96-1668-4dd7-b538-000594f408e6','rsa-generated','org.keycloak.keys.KeyProvider','faaacb96-1668-4dd7-b538-000594f408e6',NULL),('78839cf5-adba-4783-85ef-c05e53ffc8d5','Default Roles Disabled','faaacb96-1668-4dd7-b538-000594f408e6','default-roles','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','authenticated'),('7d826225-6156-4cc5-b9df-d2583f634baf','Consent Required','faaacb96-1668-4dd7-b538-000594f408e6','consent-required','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','anonymous'),('8169879e-2cf0-4305-acf0-7d83641a6653','rsa-enc-generated','faaacb96-1668-4dd7-b538-000594f408e6','rsa-enc-generated','org.keycloak.keys.KeyProvider','faaacb96-1668-4dd7-b538-000594f408e6',NULL),('896f4481-212a-4ad6-bb61-a054c8ffd1b3','Allowed Registration Web Origins','faaacb96-1668-4dd7-b538-000594f408e6','registration-web-origins','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','anonymous'),('c5658c77-575a-4f3c-878b-65cb936d59fc',NULL,'faaacb96-1668-4dd7-b538-000594f408e6','declarative-user-profile','org.keycloak.userprofile.UserProfileProvider','faaacb96-1668-4dd7-b538-000594f408e6',NULL),('d190bea7-c069-4ec2-9bae-711abf6d749a','Allowed Protocol Mapper Types','faaacb96-1668-4dd7-b538-000594f408e6','allowed-protocol-mappers','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','authenticated'),('d80a0325-ccce-4a84-9acb-f79302858217','aes-generated','faaacb96-1668-4dd7-b538-000594f408e6','aes-generated','org.keycloak.keys.KeyProvider','faaacb96-1668-4dd7-b538-000594f408e6',NULL),('db81c257-3e73-4894-a720-62f24a3e26ac','Max Clients Limit','faaacb96-1668-4dd7-b538-000594f408e6','max-clients','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','anonymous'),('e5443e9a-91f8-4e85-8fa7-7482777f6e3d','Allowed Client Scopes','faaacb96-1668-4dd7-b538-000594f408e6','allowed-client-templates','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','authenticated'),('f39f9666-72e3-4fca-84a9-5641fa1381ff','Trusted Hosts','faaacb96-1668-4dd7-b538-000594f408e6','trusted-hosts','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','anonymous'),('f8f7c6c2-302a-4662-9351-032eea8b49c0','Default Roles Disabled','faaacb96-1668-4dd7-b538-000594f408e6','default-roles','org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy','faaacb96-1668-4dd7-b538-000594f408e6','anonymous');
UNLOCK TABLES;

--
-- Dumping data for table `component_config`
--

LOCK TABLES `component_config` WRITE;
INSERT INTO `component_config` VALUES ('12ab6775-3870-459c-a949-508167076a07','d190bea7-c069-4ec2-9bae-711abf6d749a','allowed-protocol-mapper-types','oidc-address-mapper'),('13e461f4-ece1-472b-bd25-dad794d3b9a6','6e952c36-8dd0-4db2-9173-47f075f0cf5e','keyUse','SIG'),('1ff11fa0-78df-4a35-8dc0-526f132de3b9','8169879e-2cf0-4305-acf0-7d83641a6653','keyUse','ENC'),('27a019c2-aa47-4fd7-b624-7f9a64b08538','d190bea7-c069-4ec2-9bae-711abf6d749a','allowed-protocol-mapper-types','oidc-full-name-mapper'),('2dc039c4-d05e-462b-ac28-4d81b8799979','3dd53db3-b042-45ee-984f-c53c8f72f1e4','allowed-protocol-mapper-types','oidc-usermodel-property-mapper'),('32221e0b-5155-4b6b-80fb-499cc93320f9','d190bea7-c069-4ec2-9bae-711abf6d749a','allowed-protocol-mapper-types','oidc-usermodel-property-mapper'),('323051e7-7f60-4f59-a079-c4f678be5566','d80a0325-ccce-4a84-9acb-f79302858217','secret','WmX68zicJsWEHNjC6AqCRZq36UrNim_BamI5B-poSF8'),('3d087f8e-3b70-4725-9a25-2d43b055165b','6e952c36-8dd0-4db2-9173-47f075f0cf5e','privateKey','MIIEowIBAAKCAQEAvxTSRsyQp7FqIHp919f4FlCpPfaFISKF0f+V+jG3YU19Lyu2n4JBZZ9FHeaab15hSY+PqndI1WZU1whynHVTCZarwiwB0wnyOkOubg3+RGZugkvY5ltt/wYZD1vzq6nmrnLrCfFmMWq3QXsMEFnJxIHX7dj3oZEpnWr75ldsnxTmJI9uePpUWCS+3Z8SoPrUepj4aWfDtt2N0/Uhio000sf+8ekNwSTdThbaH5+E5A7zX8nk4zLKJRl9pZMkR6udu6wvwWMIyjycu7FC6Gue5mPkHhEF1cq/k4TvpXUhDOCrx9MH1ql0AqUg3tGOYTJj9X1PCJ/MgjtI6lHQv6y9GQIDAQABAoIBAADUC1TN/HTBWeTLnNnJ1jeGZ2EfVC3NCb3uB8oHKS3bte/MbXqk7KvTnoIijFw5jLUXTL14DhUcBJxhhDCrnSuNc+H5JeXyq+3Len3JddlLl5cBrnv/3NrmKzUIpA+a/euExvkWL5pzxX2gqCckNMjKFoPooE+/UpM7xqZezgoS/WLtEEddgCjJgfR+LCTZtLevXl6g+yVwMcphVRE5Lm+ofwPltsph3RJmpI4hhvVbFoqN4lBOFD0eGKtKLRd0hlvUI1xA+y3fA/N0tUs9Hu19FQcSecMLC15cgytOdQbfiKObjh8+UDgS/7bTHH1Loy2uMxpee460OvjXBFVSgkECgYEA9XvgYcQlG4Go2vHFGOg3fAnbOy8pqQJbV1Ur/ETgb68iPcsfCzhU+3ByonuQYvhawaEPhUEAkECDskq7i/IaU/vdlzljp+QvL7fJG0RE1sHTFp21HQR8rbwZQ1nbMe9bzCDt9VIcVDQXlZ6aq+csZ0xaF37g0B8t52ztAlVa2kECgYEAx0RVdemaSfD3B5iC4KWKTd62pE3U8JHcvyx2pLcSseCfd6UYE9vRa4xADhI2N/23eSTEb+ilHMRfqWApwKuFITOvVi/MRJDZdzYAStU6HmAQL0d9GElo3HRKnA+w/6IfeEwj/g3KKTmjgaiMVlbUXj4sqikSSyXKO7EfMwDivNkCgYEAt2QT/PXLwwDaZLa5yCGzUbcLUOuq89gO5O98LLpH8SelLQTR7E/pLO6UtU4aT9W5922barFk+l84A7pQ4fu8L4G5yX/WM1cE6WEjnHsj8kxapkqrQ0JW4nPja611U5i9u4HeQ6dUApPoCp6ybjoFsiYYJ/VhfhnM8VcuuM+LUAECgYAfEvzwwlkZJsafHJ1sQuRqeEyrGqgWS+jMtzZZQWNc8dZsZgZ3MlRaHSjwCM8DtEEkVyN7ACCfd9AjLafVL+o230R8gD+ugZgoCvfIs6+4hOqBNPjBDNGZb1kjNR84/iNCMz15pNTd0Os6kPoxjKDZgYCdmIINzfrXjCt9XKn/IQKBgFp/GVL8mFI/ZlAZMIVJMNRuxnU5HsPxjfWOtsAM+hbTSIybwSyZ7QzymqToNI3UksQIx1aGsGo6WnvTED8OvpUCYtqVv+HlEUnenLdzp+g3julZtu9EeKrt3dMmcFfi7rZHFIbNEcR8dbrj4djHNmNVuEHELpYQwzz3jNszZlEU'),('3e7b563f-bd99-4575-9dea-9d92c92ea35f','135dd8bf-8022-40d8-8ac9-5d6a5040aa5c','kid','df8b2d55-1233-4f0d-8fb7-560f851277cc'),('480c09ff-0530-4238-a80b-90dc4f66987b','135dd8bf-8022-40d8-8ac9-5d6a5040aa5c','algorithm','HS512'),('4849ec44-ddf4-44c2-b6b1-b64cee0240f2','8169879e-2cf0-4305-acf0-7d83641a6653','certificate','MIICmzCCAYMCBgGhv1hMRTANBgkqhkiG9w0BAQsFADARMQ8wDQYDVQQDDAZtYXN0ZXIwHhcNMjYxMTA5MDgwNDU3WhcNMzYxMTA5MDgwNjM3WjARMQ8wDQYDVQQDDAZtYXN0ZXIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC5R6Nqc7ohdNli/U94C4cFRI62GxZIAsPgp6Cpbfky851jVvVhhT/+zXA2lMf6/0bcMP8FblECbDTDMzmgghB0hKYvuT1AfVC1vCyM8RR9RUiW1vkXyswhBybtNN0MupkcajW5xmECLSe+mx8kvlDDPOYqV65vhifXiDuuvUNmfJ9GbJCLRzvRW6N7A4l4fdQfqDBkdSgRMldTggjGvo6fT60NvrSV5lwGO45DZ5eb5MPddIsdhZrPdZaPe5fmWeeAcypWLVGy0suKnkZ68BIjOvQnDqpr7X/1tCCgY8xvZRIVX7umVvappfymaoKnY5RXX51rpZP3Nvq/OYPSsxjzAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAFhXout0qX5VUoo2aZeIWcCAR++Mw8vphtitMsPR4xFIF9HCcPrtPoqnNmL1dmQ03YvzE6N2LkbMYe4lCSzTF9m+9t5SeXUW8D+HAot/Eo2W/GL31UhOvVgA5gJ9uKL2yN7UhIwPD3tv1IVLAnzX4lMn/rDfQ+EgOOTH5J+SZIgoexJbRNubxT5YWw09nKxj9Qo9WE/gQ0iLmVXP4nbC6ss7DRBNmYTWzluarw2jvlQ7HIV/tkz1d3cpSq3PjhQkO//pTDrCi97Vy1zHiN67QIQdnJa7CcAFLL1M49cn6rd4+Zovj9sIkDcJC7ykf63KhGBTDwo/OV8we/B10gI/xyk='),('494953ef-e115-4bfa-8900-b18f0b3a9838','8169879e-2cf0-4305-acf0-7d83641a6653','algorithm','RSA-OAEP'),('547e994c-abf6-4234-9f3d-ff9819a91f44','d190bea7-c069-4ec2-9bae-711abf6d749a','allowed-protocol-mapper-types','saml-user-property-mapper'),('555c594c-3f36-40bf-a66b-d3f803461860','3dd53db3-b042-45ee-984f-c53c8f72f1e4','allowed-protocol-mapper-types','oidc-usermodel-attribute-mapper'),('5914867e-7eb1-43d7-bde2-2626a888b2eb','d190bea7-c069-4ec2-9bae-711abf6d749a','allowed-protocol-mapper-types','saml-role-list-mapper'),('5a3db618-2b28-443d-bac3-038fbe8728d6','135dd8bf-8022-40d8-8ac9-5d6a5040aa5c','secret','0Y4Z8JHgQb-355zfy31oOwokMF8jYkvRVy1J8oJASn3Pg0J1exdZ0sE_tjuUB1uh_bTLqh-Yr4yP732P6RmrBFL4YEcKbdbuAo380ae5bT4Zr3NoXDxh2vmSOLPAgyNbt18MXDmJl2MVjG2GXkmr2mYY_8FVjYEXKfH1jNTfI_Y'),('61382eea-9f14-4581-addb-af6a2ae963b4','8169879e-2cf0-4305-acf0-7d83641a6653','privateKey','MIIEogIBAAKCAQEAuUejanO6IXTZYv1PeAuHBUSOthsWSALD4KegqW35MvOdY1b1YYU//s1wNpTH+v9G3DD/BW5RAmw0wzM5oIIQdISmL7k9QH1QtbwsjPEUfUVIltb5F8rMIQcm7TTdDLqZHGo1ucZhAi0nvpsfJL5QwzzmKleub4Yn14g7rr1DZnyfRmyQi0c70VujewOJeH3UH6gwZHUoETJXU4IIxr6On0+tDb60leZcBjuOQ2eXm+TD3XSLHYWaz3WWj3uX5lnngHMqVi1RstLLip5GevASIzr0Jw6qa+1/9bQgoGPMb2USFV+7plb2qaX8pmqCp2OUV1+da6WT9zb6vzmD0rMY8wIDAQABAoIBAFOnarsnoUR106kEIhtbaQ0R1TWXqUm+Jd6LENku1DMTF17A5m2vkiNjcmTSbDCBjebhIGO9WUo0vOXdfQlhcDiLo9UsV+GEMyq62YqRVuTwoUOpsDHz2JKY/hRfp+aVYYgY1EUasrYe2TEQLNGUNDbSikFX8WRdOCPyWLAeuA3PNg9cPXn1kOKMMYGOY+joiySazJx3I34ab4nAVNUrTjSj7DogJUU9YOFzJRxLhCN+U5QxbopRV/fNgsBhW3ghDDdgyHDUmE/Az3g/ulHC0PfVkSBiTiYEcAmjmRe+rmpsDlnfoyyFg6XDOHNKOSX43Yja3FzndDwiEX2dsqkC7RECgYEA3eztB1URn4zTu/MlhHB1topdSVQOfY3AEozrbgqsN4K7q25C+8yMEmhFI8CsBma1dIUTS7ad692hAkAF0z/TKXvQvW02V/48An+OzSoqofD90pQqRvNyw2K4nzq+gLmULibyffNO4D86+XxR1/kjv1rU5yABDGf27YFXmkgqnaUCgYEA1bpOgkntDRDfJXpoBE+KqtYKnGPbM/5VerVAbgKmZDF6rzC9bVU1WCT+/lqDxzO+n2KUedY8BDRh/j29nLO09LoZ57snhKWK+VgrkbwTVKlMDjHX/rG/bfuMabb48BAvq5fKPIEJb4zpuK/ymJRzQt0miJ4B2lL2o0NA4wduSLcCgYBZke2c3v3M6pburdU/nfA0q6W5Gd77V8Hk+tFuyYn2oaJDL66DWGxUZZc6NeJ4du3XyHogPeWBNCNu+A4h1AnTHXEDc1fSrf7kdz1YmyM31z9qxXhGyK1SJL8lLR2EcOJYukl3AkOciIix9zZFN/3wlqWFX0ptCm0EMQb9cxEYLQKBgGnSakbmVYHPpb0Hw3LG83Css+pFIua2ehpcnf8aPsqDGSye5Fu7AcOX5c2IgZDjFPITvFIq+eJXEWHxre1lqSY28tai+ukZkhrtRf1NcwDLJkYs9bY8yfypvRcmqlEqon/Ckzar6UEbMynnrCVR81Pa7dZc7avswgOKLBl8t2U3AoGAbPsQMRG5feuPFlAKhzCWME9QH2/lguTjywp28lERrsHYhSezetoYxIv7ROS+0ebS3JOGnKsHZ9W5sPtvjBM1RiyV13uLo+7OH1e0pmRv3a8xFJabNK0G5CUiy+7wyI84JVe5GgHQcC3m7Dx69+bifRtSLcwe/yvGedltey/MsKk='),('674d45ba-a3ee-4ddb-b4ff-493b198bdf97','3dd53db3-b042-45ee-984f-c53c8f72f1e4','allowed-protocol-mapper-types','saml-role-list-mapper'),('6ed3f1fe-a79b-4db6-9568-9e904abc23de','3dd53db3-b042-45ee-984f-c53c8f72f1e4','allowed-protocol-mapper-types','saml-user-property-mapper'),('7562004a-e784-4c4a-861f-39ff0ffab32b','6e952c36-8dd0-4db2-9173-47f075f0cf5e','certificate','MIICmzCCAYMCBgGhv1hLbDANBgkqhkiG9w0BAQsFADARMQ8wDQYDVQQDDAZtYXN0ZXIwHhcNMjYxMTA5MDgwNDU3WhcNMzYxMTA5MDgwNjM3WjARMQ8wDQYDVQQDDAZtYXN0ZXIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC/FNJGzJCnsWogen3X1/gWUKk99oUhIoXR/5X6MbdhTX0vK7afgkFln0Ud5ppvXmFJj4+qd0jVZlTXCHKcdVMJlqvCLAHTCfI6Q65uDf5EZm6CS9jmW23/BhkPW/OrqeaucusJ8WYxardBewwQWcnEgdft2PehkSmdavvmV2yfFOYkj254+lRYJL7dnxKg+tR6mPhpZ8O23Y3T9SGKjTTSx/7x6Q3BJN1OFtofn4TkDvNfyeTjMsolGX2lkyRHq527rC/BYwjKPJy7sULoa57mY+QeEQXVyr+ThO+ldSEM4KvH0wfWqXQCpSDe0Y5hMmP1fU8In8yCO0jqUdC/rL0ZAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAAAaEoCI625TqLfIdhWwop1BNWVnXhxwW7S8etVAPt1fqPLSxHL0Ok2Bn5cHWLagA8va4uUZDDTol4q7V65ZkEDspxr4ND63afRdkIfh9PzEpUGFe+OwmooljqbfdSlHlaSKLk5BrNpw4gbD2yuMX98a8VrHGBwSPUHGm+ylHEaC7UM0KXYkhL5+JvjPZK8yUGhqGcaQw19hGBI0tdPscZ5SroerzvTuWP0SwJpJKN30Ux/V+34Qk56YoKabwm0B/oJoXEpJkIi5nO/D+U0h2KFlEx2s3ORn/PC1VdfZhfG9ZhTjLRiC+BPO3qpeDT8ZgXnIO0vvUr5nNLS6opQt7TA='),('75ee2322-c7a1-40a4-b600-5fe21497aa3c','6ba2be1a-f0bc-445e-b8c6-21aa9f7ce9eb','allow-default-scopes','true'),('812dc735-b8c9-47e7-9249-8e43f32e1705','e5443e9a-91f8-4e85-8fa7-7482777f6e3d','allow-default-scopes','true'),('83c720f3-ca66-498e-8f3e-557773395adb','f39f9666-72e3-4fca-84a9-5641fa1381ff','host-sending-registration-request-must-match','true'),('849a56cb-e8bf-447a-a2f7-321784337a14','f39f9666-72e3-4fca-84a9-5641fa1381ff','client-uris-must-match','true'),('89d4152f-521d-4d76-92da-caf90657d061','d190bea7-c069-4ec2-9bae-711abf6d749a','allowed-protocol-mapper-types','saml-user-attribute-mapper'),('8c1b6e22-3d41-4584-bc9e-cb962128e4eb','3dd53db3-b042-45ee-984f-c53c8f72f1e4','allowed-protocol-mapper-types','oidc-sha256-pairwise-sub-mapper'),('a228725b-2189-4f15-bd16-fba63c19ca06','3dd53db3-b042-45ee-984f-c53c8f72f1e4','allowed-protocol-mapper-types','oidc-full-name-mapper'),('a5e19d9d-91c1-4bfa-b7d4-937fa7fee4ef','d80a0325-ccce-4a84-9acb-f79302858217','priority','100'),('b92e84be-905e-46db-99e6-85bee4bfe19d','3dd53db3-b042-45ee-984f-c53c8f72f1e4','allowed-protocol-mapper-types','saml-user-attribute-mapper'),('baad7b88-2c2a-424c-a082-6a2655d49dfe','d190bea7-c069-4ec2-9bae-711abf6d749a','allowed-protocol-mapper-types','oidc-usermodel-attribute-mapper'),('cd7da363-c702-4901-ba60-a6980116c970','6e952c36-8dd0-4db2-9173-47f075f0cf5e','priority','100'),('d477c652-bfab-4957-8987-a346e078d99a','c5658c77-575a-4f3c-878b-65cb936d59fc','kc.user.profile.config','{\"attributes\":[{\"name\":\"username\",\"displayName\":\"${username}\",\"validations\":{\"length\":{\"min\":3,\"max\":255},\"username-prohibited-characters\":{},\"up-username-not-idn-homograph\":{}},\"permissions\":{\"view\":[\"admin\",\"user\"],\"edit\":[\"admin\",\"user\"]},\"multivalued\":false},{\"name\":\"email\",\"displayName\":\"${email}\",\"validations\":{\"email\":{},\"length\":{\"max\":255}},\"permissions\":{\"view\":[\"admin\",\"user\"],\"edit\":[\"admin\",\"user\"]},\"multivalued\":false},{\"name\":\"firstName\",\"displayName\":\"${firstName}\",\"validations\":{\"length\":{\"max\":255},\"person-name-prohibited-characters\":{}},\"permissions\":{\"view\":[\"admin\",\"user\"],\"edit\":[\"admin\",\"user\"]},\"multivalued\":false},{\"name\":\"lastName\",\"displayName\":\"${lastName}\",\"validations\":{\"length\":{\"max\":255},\"person-name-prohibited-characters\":{}},\"permissions\":{\"view\":[\"admin\",\"user\"],\"edit\":[\"admin\",\"user\"]},\"multivalued\":false}],\"groups\":[{\"name\":\"user-metadata\",\"displayHeader\":\"User metadata\",\"displayDescription\":\"Attributes, which refer to user metadata\"}]}'),('d79a5ebe-56d7-422c-a743-184475f63a40','3dd53db3-b042-45ee-984f-c53c8f72f1e4','allowed-protocol-mapper-types','oidc-address-mapper'),('dd819304-1a84-43f8-93a3-a53236c78341','d190bea7-c069-4ec2-9bae-711abf6d749a','allowed-protocol-mapper-types','oidc-sha256-pairwise-sub-mapper'),('e0723aff-88a0-4087-a2e0-9038d7d86eb8','8169879e-2cf0-4305-acf0-7d83641a6653','priority','100'),('e49158e7-8a5d-4c4f-9f36-7d9aa8c5a574','135dd8bf-8022-40d8-8ac9-5d6a5040aa5c','priority','100'),('ebfda45d-7d64-4f9d-9881-3264e9cac895','db81c257-3e73-4894-a720-62f24a3e26ac','max-clients','200'),('f34cfb53-8b44-45b1-88f3-894113bf4c83','d80a0325-ccce-4a84-9acb-f79302858217','kid','5f358409-e9cf-484a-a6d7-a96c4e08e1cc');
UNLOCK TABLES;

--
-- Dumping data for table `composite_role`
--

LOCK TABLES `composite_role` WRITE;
INSERT INTO `composite_role` VALUES ('2dc0db2c-d02d-49ce-b1b6-e57923fd2129','7a5d36bc-d21b-43a2-9887-7dd788f10103'),('51fef47e-159b-4675-9b5c-3a3e51dc62fc','fd9c0ffc-48a7-48ea-bd44-88f0908b2328'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','103e63e0-b7bc-47b0-88ca-c13c11eecb1b'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','2dc0db2c-d02d-49ce-b1b6-e57923fd2129'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','352e2bda-e324-4a7f-83b5-219802c4c320'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','3a2b8342-ae3f-4ad6-8a4a-c019aa3dab3a'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','40d9509c-23b2-4d95-87cd-214e7abb7281'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','4e020b36-c21c-4d99-93d2-d1a983060944'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','51fef47e-159b-4675-9b5c-3a3e51dc62fc'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','73437c5b-2dcc-4b96-adb2-9df7e255657c'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','7a5d36bc-d21b-43a2-9887-7dd788f10103'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','8165d16d-fedb-40bb-ad8c-bfaa90dc272b'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','888cbfc4-6b0a-4f5b-8414-ebb46446d0c3'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','9e2f1ea3-984b-4f15-b7b9-92eb20587846'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','9f0ed45c-f548-4d3a-8735-8759c25ff57e'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','c17b1f42-9790-4707-993b-0ab08996ed40'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','cd64029d-f471-44e3-882a-ae09917598db'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','cd6a7c4c-99bf-444d-91fe-96ac7fc5be30'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','d047fd38-c752-4bc8-8ed5-a36cde9021eb'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','d24cd467-86fd-4c12-8d2b-242f6ff49ef9'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','d478be7f-f0b3-4a09-9fbd-3433ff355d22'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','d4f67f7b-ce5c-494d-9a7d-4af24331c2b7'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','e55b2fd6-f709-43cf-a676-ddb2dfc25fca'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','fd9c0ffc-48a7-48ea-bd44-88f0908b2328'),('8b0cd07f-ad78-4aaf-bca9-dc7e7eb787ae','d2386173-4443-4607-b04c-a14ec55f8bdd'),('cd6a7c4c-99bf-444d-91fe-96ac7fc5be30','103e63e0-b7bc-47b0-88ca-c13c11eecb1b'),('cd6a7c4c-99bf-444d-91fe-96ac7fc5be30','73437c5b-2dcc-4b96-adb2-9df7e255657c'),('d463aee3-b627-4ca9-8d71-c2b46b1364af','455d5e7c-72c5-4557-9544-ebcfe8e9a234'),('d463aee3-b627-4ca9-8d71-c2b46b1364af','8b0cd07f-ad78-4aaf-bca9-dc7e7eb787ae'),('d463aee3-b627-4ca9-8d71-c2b46b1364af','b273ad17-cbac-4a38-b417-f349a6a39bfe'),('d463aee3-b627-4ca9-8d71-c2b46b1364af','fe0685cc-69a7-4ea3-ac18-e725bd257988'),('eaeb0a6c-deda-439b-bd3c-4153206571c9','ee3990a6-0747-436e-a585-1e220d129b66');
UNLOCK TABLES;

--
-- Dumping data for table `credential`
--

LOCK TABLES `credential` WRITE;
INSERT INTO `credential` VALUES ('b7c419de-9986-45d6-8852-72b6c590ee41',NULL,'password','3e7ffc4a-1e47-4508-b506-4e21d9458ce1',1794211597907,NULL,'{\"value\":\"Wav0X/bWAubEf1d7tg9Lr/7e/TgUYO5qKgB5JDzh020=\",\"salt\":\"8UrvMIF8SbuQ6B4/4HGGQQ==\",\"additionalParameters\":{}}','{\"hashIterations\":5,\"algorithm\":\"argon2\",\"additionalParameters\":{\"hashLength\":[\"32\"],\"memory\":[\"7168\"],\"type\":[\"id\"],\"version\":[\"1.3\"],\"parallelism\":[\"1\"]}}',10,0);
UNLOCK TABLES;

--
-- Dumping data for table `databasechangelog`
--

LOCK TABLES `databasechangelog` WRITE;
INSERT INTO `databasechangelog` VALUES ('1.0.0.Final-KEYCLOAK-5461','sthorger@redhat.com','META-INF/db2-jpa-changelog-1.0.0.Final.xml','2026-11-09 17:06:14',2,'MARK_RAN','9:828775b1596a07d1200ba1d49e5e3941','createTable tableName=APPLICATION_DEFAULT_ROLES; createTable tableName=CLIENT; createTable tableName=CLIENT_SESSION; createTable tableName=CLIENT_SESSION_ROLE; createTable tableName=COMPOSITE_ROLE; createTable tableName=CREDENTIAL; createTable tab...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.0.0.Final-KEYCLOAK-5461','sthorger@redhat.com','META-INF/jpa-changelog-1.0.0.Final.xml','2026-11-09 17:06:14',1,'EXECUTED','9:6f1016664e21e16d26517a4418f5e3df','createTable tableName=APPLICATION_DEFAULT_ROLES; createTable tableName=CLIENT; createTable tableName=CLIENT_SESSION; createTable tableName=CLIENT_SESSION_ROLE; createTable tableName=COMPOSITE_ROLE; createTable tableName=CREDENTIAL; createTable tab...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.1.0.Beta1','sthorger@redhat.com','META-INF/jpa-changelog-1.1.0.Beta1.xml','2026-11-09 17:06:15',3,'EXECUTED','9:5f090e44a7d595883c1fb61f4b41fd38','delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION; createTable tableName=CLIENT_ATTRIBUTES; createTable tableName=CLIENT_SESSION_NOTE; createTable tableName=APP_NODE_REGISTRATIONS; addColumn table...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.1.0.Final','sthorger@redhat.com','META-INF/jpa-changelog-1.1.0.Final.xml','2026-11-09 17:06:15',4,'EXECUTED','9:c07e577387a3d2c04d1adc9aaad8730e','renameColumn newColumnName=EVENT_TIME, oldColumnName=TIME, tableName=EVENT_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.2.0.Beta1','psilva@redhat.com','META-INF/db2-jpa-changelog-1.2.0.Beta1.xml','2026-11-09 17:06:15',6,'MARK_RAN','9:543b5c9989f024fe35c6f6c5a97de88e','delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION; createTable tableName=PROTOCOL_MAPPER; createTable tableName=PROTOCOL_MAPPER_CONFIG; createTable tableName=...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.2.0.Beta1','psilva@redhat.com','META-INF/jpa-changelog-1.2.0.Beta1.xml','2026-11-09 17:06:15',5,'EXECUTED','9:b68ce996c655922dbcd2fe6b6ae72686','delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION; createTable tableName=PROTOCOL_MAPPER; createTable tableName=PROTOCOL_MAPPER_CONFIG; createTable tableName=...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.2.0.Final','keycloak','META-INF/jpa-changelog-1.2.0.Final.xml','2026-11-09 17:06:16',9,'EXECUTED','9:9d05c7be10cdb873f8bcb41bc3a8ab23','update tableName=CLIENT; update tableName=CLIENT; update tableName=CLIENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.2.0.RC1','bburke@redhat.com','META-INF/db2-jpa-changelog-1.2.0.CR1.xml','2026-11-09 17:06:16',8,'MARK_RAN','9:db4a145ba11a6fdaefb397f6dbf829a1','delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete tableName=USER_SESSION; createTable tableName=MIGRATION_MODEL; createTable tableName=IDENTITY_P...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.2.0.RC1','bburke@redhat.com','META-INF/jpa-changelog-1.2.0.CR1.xml','2026-11-09 17:06:16',7,'EXECUTED','9:765afebbe21cf5bbca048e632df38336','delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete tableName=USER_SESSION; createTable tableName=MIGRATION_MODEL; createTable tableName=IDENTITY_P...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.3.0','bburke@redhat.com','META-INF/jpa-changelog-1.3.0.xml','2026-11-09 17:06:17',10,'EXECUTED','9:18593702353128d53111f9b1ff0b82b8','delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_PROT_MAPPER; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete tableName=USER_SESSION; createTable tableName=ADMI...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.4.0','bburke@redhat.com','META-INF/db2-jpa-changelog-1.4.0.xml','2026-11-09 17:06:17',12,'MARK_RAN','9:e1ff28bf7568451453f844c5d54bb0b5','delete tableName=CLIENT_SESSION_AUTH_STATUS; delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_PROT_MAPPER; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete table...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.4.0','bburke@redhat.com','META-INF/jpa-changelog-1.4.0.xml','2026-11-09 17:06:17',11,'EXECUTED','9:6122efe5f090e41a85c0f1c9e52cbb62','delete tableName=CLIENT_SESSION_AUTH_STATUS; delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_PROT_MAPPER; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete table...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.5.0','bburke@redhat.com','META-INF/jpa-changelog-1.5.0.xml','2026-11-09 17:06:17',13,'EXECUTED','9:7af32cd8957fbc069f796b61217483fd','delete tableName=CLIENT_SESSION_AUTH_STATUS; delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_PROT_MAPPER; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete table...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.6.1','mposolda@redhat.com','META-INF/jpa-changelog-1.6.1.xml','2026-11-09 17:06:18',17,'EXECUTED','9:d41d8cd98f00b204e9800998ecf8427e','empty','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.6.1_from15','mposolda@redhat.com','META-INF/jpa-changelog-1.6.1.xml','2026-11-09 17:06:18',14,'EXECUTED','9:6005e15e84714cd83226bf7879f54190','addColumn tableName=REALM; addColumn tableName=KEYCLOAK_ROLE; addColumn tableName=CLIENT; createTable tableName=OFFLINE_USER_SESSION; createTable tableName=OFFLINE_CLIENT_SESSION; addPrimaryKey constraintName=CONSTRAINT_OFFL_US_SES_PK2, tableName=...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.6.1_from16','mposolda@redhat.com','META-INF/jpa-changelog-1.6.1.xml','2026-11-09 17:06:18',16,'MARK_RAN','9:f8dadc9284440469dcf71e25ca6ab99b','dropPrimaryKey constraintName=CONSTRAINT_OFFLINE_US_SES_PK, tableName=OFFLINE_USER_SESSION; dropPrimaryKey constraintName=CONSTRAINT_OFFLINE_CL_SES_PK, tableName=OFFLINE_CLIENT_SESSION; addColumn tableName=OFFLINE_USER_SESSION; update tableName=OF...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.6.1_from16-pre','mposolda@redhat.com','META-INF/jpa-changelog-1.6.1.xml','2026-11-09 17:06:18',15,'MARK_RAN','9:bf656f5a2b055d07f314431cae76f06c','delete tableName=OFFLINE_CLIENT_SESSION; delete tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.7.0','bburke@redhat.com','META-INF/jpa-changelog-1.7.0.xml','2026-11-09 17:06:18',18,'EXECUTED','9:3368ff0be4c2855ee2dd9ca813b38d8e','createTable tableName=KEYCLOAK_GROUP; createTable tableName=GROUP_ROLE_MAPPING; createTable tableName=GROUP_ATTRIBUTE; createTable tableName=USER_GROUP_MEMBERSHIP; createTable tableName=REALM_DEFAULT_GROUPS; addColumn tableName=IDENTITY_PROVIDER; ...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.8.0','mposolda@redhat.com','META-INF/db2-jpa-changelog-1.8.0.xml','2026-11-09 17:06:18',21,'MARK_RAN','9:831e82914316dc8a57dc09d755f23c51','addColumn tableName=IDENTITY_PROVIDER; createTable tableName=CLIENT_TEMPLATE; createTable tableName=CLIENT_TEMPLATE_ATTRIBUTES; createTable tableName=TEMPLATE_SCOPE_MAPPING; dropNotNullConstraint columnName=CLIENT_ID, tableName=PROTOCOL_MAPPER; ad...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.8.0','mposolda@redhat.com','META-INF/jpa-changelog-1.8.0.xml','2026-11-09 17:06:18',19,'EXECUTED','9:8ac2fb5dd030b24c0570a763ed75ed20','addColumn tableName=IDENTITY_PROVIDER; createTable tableName=CLIENT_TEMPLATE; createTable tableName=CLIENT_TEMPLATE_ATTRIBUTES; createTable tableName=TEMPLATE_SCOPE_MAPPING; dropNotNullConstraint columnName=CLIENT_ID, tableName=PROTOCOL_MAPPER; ad...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.8.0-2','keycloak','META-INF/db2-jpa-changelog-1.8.0.xml','2026-11-09 17:06:18',22,'MARK_RAN','9:f91ddca9b19743db60e3057679810e6c','dropDefaultValue columnName=ALGORITHM, tableName=CREDENTIAL; update tableName=CREDENTIAL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.8.0-2','keycloak','META-INF/jpa-changelog-1.8.0.xml','2026-11-09 17:06:18',20,'EXECUTED','9:f91ddca9b19743db60e3057679810e6c','dropDefaultValue columnName=ALGORITHM, tableName=CREDENTIAL; update tableName=CREDENTIAL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.9.0','mposolda@redhat.com','META-INF/jpa-changelog-1.9.0.xml','2026-11-09 17:06:18',23,'EXECUTED','9:bc3d0f9e823a69dc21e23e94c7a94bb1','update tableName=REALM; update tableName=REALM; update tableName=REALM; update tableName=REALM; update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=REALM; update tableName=REALM; customChange; dr...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.9.1','keycloak','META-INF/db2-jpa-changelog-1.9.1.xml','2026-11-09 17:06:18',25,'MARK_RAN','9:0d6c65c6f58732d81569e77b10ba301d','modifyDataType columnName=PRIVATE_KEY, tableName=REALM; modifyDataType columnName=CERTIFICATE, tableName=REALM','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.9.1','keycloak','META-INF/jpa-changelog-1.9.1.xml','2026-11-09 17:06:18',24,'EXECUTED','9:c9999da42f543575ab790e76439a2679','modifyDataType columnName=PRIVATE_KEY, tableName=REALM; modifyDataType columnName=PUBLIC_KEY, tableName=REALM; modifyDataType columnName=CERTIFICATE, tableName=REALM','',NULL,'4.33.0',NULL,NULL,'4211565042'),('1.9.2','keycloak','META-INF/jpa-changelog-1.9.2.xml','2026-11-09 17:06:19',26,'EXECUTED','9:fc576660fc016ae53d2d4778d84d86d0','createIndex indexName=IDX_USER_EMAIL, tableName=USER_ENTITY; createIndex indexName=IDX_USER_ROLE_MAPPING, tableName=USER_ROLE_MAPPING; createIndex indexName=IDX_USER_GROUP_MAPPING, tableName=USER_GROUP_MEMBERSHIP; createIndex indexName=IDX_USER_CO...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('12.1.0-add-realm-localization-table','keycloak','META-INF/jpa-changelog-12.0.0.xml','2026-11-09 17:06:25',88,'EXECUTED','9:fffabce2bc01e1a8f5110d5278500065','createTable tableName=REALM_LOCALIZATIONS; addPrimaryKey tableName=REALM_LOCALIZATIONS','',NULL,'4.33.0',NULL,NULL,'4211565042'),('13.0.0-increase-column-size-federated','keycloak','META-INF/jpa-changelog-13.0.0.xml','2026-11-09 17:06:25',94,'EXECUTED','9:43c0c1055b6761b4b3e89de76d612ccf','modifyDataType columnName=CLIENT_ID, tableName=CLIENT_SCOPE_CLIENT; modifyDataType columnName=SCOPE_ID, tableName=CLIENT_SCOPE_CLIENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('13.0.0-KEYCLOAK-16844','keycloak','META-INF/jpa-changelog-13.0.0.xml','2026-11-09 17:06:25',91,'EXECUTED','9:ad1194d66c937e3ffc82386c050ba089','createIndex indexName=IDX_OFFLINE_USS_PRELOAD, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('13.0.0-KEYCLOAK-17992-drop-constraints','keycloak','META-INF/jpa-changelog-13.0.0.xml','2026-11-09 17:06:25',93,'MARK_RAN','9:544d201116a0fcc5a5da0925fbbc3bde','dropPrimaryKey constraintName=C_CLI_SCOPE_BIND, tableName=CLIENT_SCOPE_CLIENT; dropIndex indexName=IDX_CLSCOPE_CL, tableName=CLIENT_SCOPE_CLIENT; dropIndex indexName=IDX_CL_CLSCOPE, tableName=CLIENT_SCOPE_CLIENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('13.0.0-KEYCLOAK-17992-recreate-constraints','keycloak','META-INF/jpa-changelog-13.0.0.xml','2026-11-09 17:06:25',95,'MARK_RAN','9:8bd711fd0330f4fe980494ca43ab1139','addNotNullConstraint columnName=CLIENT_ID, tableName=CLIENT_SCOPE_CLIENT; addNotNullConstraint columnName=SCOPE_ID, tableName=CLIENT_SCOPE_CLIENT; addPrimaryKey constraintName=C_CLI_SCOPE_BIND, tableName=CLIENT_SCOPE_CLIENT; createIndex indexName=...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('14.0.0-KEYCLOAK-11019','keycloak','META-INF/jpa-changelog-14.0.0.xml','2026-11-09 17:06:26',97,'EXECUTED','9:24fb8611e97f29989bea412aa38d12b7','createIndex indexName=IDX_OFFLINE_CSS_PRELOAD, tableName=OFFLINE_CLIENT_SESSION; createIndex indexName=IDX_OFFLINE_USS_BY_USER, tableName=OFFLINE_USER_SESSION; createIndex indexName=IDX_OFFLINE_USS_BY_USERSESS, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('14.0.0-KEYCLOAK-18286','keycloak','META-INF/jpa-changelog-14.0.0.xml','2026-11-09 17:06:26',98,'MARK_RAN','9:259f89014ce2506ee84740cbf7163aa7','createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('14.0.0-KEYCLOAK-18286-revert','keycloak','META-INF/jpa-changelog-14.0.0.xml','2026-11-09 17:06:26',99,'MARK_RAN','9:04baaf56c116ed19951cbc2cca584022','dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('14.0.0-KEYCLOAK-18286-supported-dbs','keycloak','META-INF/jpa-changelog-14.0.0.xml','2026-11-09 17:06:26',100,'EXECUTED','9:bd2bd0fc7768cf0845ac96a8786fa735','createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('14.0.0-KEYCLOAK-18286-unsupported-dbs','keycloak','META-INF/jpa-changelog-14.0.0.xml','2026-11-09 17:06:26',101,'MARK_RAN','9:d3d977031d431db16e2c181ce49d73e9','createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('15.0.0-KEYCLOAK-18467','keycloak','META-INF/jpa-changelog-15.0.0.xml','2026-11-09 17:06:26',104,'EXECUTED','9:47a760639ac597360a8219f5b768b4de','addColumn tableName=REALM_LOCALIZATIONS; update tableName=REALM_LOCALIZATIONS; dropColumn columnName=TEXTS, tableName=REALM_LOCALIZATIONS; renameColumn newColumnName=TEXTS, oldColumnName=TEXTS_NEW, tableName=REALM_LOCALIZATIONS; addNotNullConstrai...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('17.0.0-9562','keycloak','META-INF/jpa-changelog-17.0.0.xml','2026-11-09 17:06:26',105,'EXECUTED','9:a6272f0576727dd8cad2522335f5d99e','createIndex indexName=IDX_USER_SERVICE_ACCOUNT, tableName=USER_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('18.0.0-10625-IDX_ADMIN_EVENT_TIME','keycloak','META-INF/jpa-changelog-18.0.0.xml','2026-11-09 17:06:26',106,'EXECUTED','9:015479dbd691d9cc8669282f4828c41d','createIndex indexName=IDX_ADMIN_EVENT_TIME, tableName=ADMIN_EVENT_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('18.0.15-30992-index-consent','keycloak','META-INF/jpa-changelog-18.0.15.xml','2026-11-09 17:06:26',107,'EXECUTED','9:80071ede7a05604b1f4906f3bf3b00f0','createIndex indexName=IDX_USCONSENT_SCOPE_ID, tableName=USER_CONSENT_CLIENT_SCOPE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('19.0.0-10135','keycloak','META-INF/jpa-changelog-19.0.0.xml','2026-11-09 17:06:26',108,'EXECUTED','9:9518e495fdd22f78ad6425cc30630221','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.1.0-KEYCLOAK-5461','bburke@redhat.com','META-INF/jpa-changelog-2.1.0.xml','2026-11-09 17:06:20',29,'EXECUTED','9:bd88e1f833df0420b01e114533aee5e8','createTable tableName=BROKER_LINK; createTable tableName=FED_USER_ATTRIBUTE; createTable tableName=FED_USER_CONSENT; createTable tableName=FED_USER_CONSENT_ROLE; createTable tableName=FED_USER_CONSENT_PROT_MAPPER; createTable tableName=FED_USER_CR...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.2.0','bburke@redhat.com','META-INF/jpa-changelog-2.2.0.xml','2026-11-09 17:06:20',30,'EXECUTED','9:a7022af5267f019d020edfe316ef4371','addColumn tableName=ADMIN_EVENT_ENTITY; createTable tableName=CREDENTIAL_ATTRIBUTE; createTable tableName=FED_CREDENTIAL_ATTRIBUTE; modifyDataType columnName=VALUE, tableName=CREDENTIAL; addForeignKeyConstraint baseTableName=FED_CREDENTIAL_ATTRIBU...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.3.0','bburke@redhat.com','META-INF/jpa-changelog-2.3.0.xml','2026-11-09 17:06:20',31,'EXECUTED','9:fc155c394040654d6a79227e56f5e25a','createTable tableName=FEDERATED_USER; addPrimaryKey constraintName=CONSTR_FEDERATED_USER, tableName=FEDERATED_USER; dropDefaultValue columnName=TOTP, tableName=USER_ENTITY; dropColumn columnName=TOTP, tableName=USER_ENTITY; addColumn tableName=IDE...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.4.0','bburke@redhat.com','META-INF/jpa-changelog-2.4.0.xml','2026-11-09 17:06:20',32,'EXECUTED','9:eac4ffb2a14795e5dc7b426063e54d88','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.5.0','bburke@redhat.com','META-INF/jpa-changelog-2.5.0.xml','2026-11-09 17:06:20',33,'EXECUTED','9:54937c05672568c4c64fc9524c1e9462','customChange; modifyDataType columnName=USER_ID, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.5.0-duplicate-email-support','slawomir@dabek.name','META-INF/jpa-changelog-2.5.0.xml','2026-11-09 17:06:20',36,'EXECUTED','9:61b6d3d7a4c0e0024b0c839da283da0c','addColumn tableName=REALM','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.5.0-unicode-oracle','hmlnarik@redhat.com','META-INF/jpa-changelog-2.5.0.xml','2026-11-09 17:06:20',34,'MARK_RAN','9:737ee933fd399814ed5e24f3b1bbe39d','modifyDataType columnName=DESCRIPTION, tableName=AUTHENTICATION_FLOW; modifyDataType columnName=DESCRIPTION, tableName=CLIENT_TEMPLATE; modifyDataType columnName=DESCRIPTION, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=DESCRIPTION,...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.5.0-unicode-other-dbs','hmlnarik@redhat.com','META-INF/jpa-changelog-2.5.0.xml','2026-11-09 17:06:20',35,'EXECUTED','9:33d72168746f81f98ae3a1e8e0ca3554','modifyDataType columnName=DESCRIPTION, tableName=AUTHENTICATION_FLOW; modifyDataType columnName=DESCRIPTION, tableName=CLIENT_TEMPLATE; modifyDataType columnName=DESCRIPTION, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=DESCRIPTION,...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.5.0-unique-group-names','hmlnarik@redhat.com','META-INF/jpa-changelog-2.5.0.xml','2026-11-09 17:06:20',37,'EXECUTED','9:8dcac7bdf7378e7d823cdfddebf72fda','addUniqueConstraint constraintName=SIBLING_NAMES, tableName=KEYCLOAK_GROUP','',NULL,'4.33.0',NULL,NULL,'4211565042'),('2.5.1','bburke@redhat.com','META-INF/jpa-changelog-2.5.1.xml','2026-11-09 17:06:20',38,'EXECUTED','9:a2b870802540cb3faa72098db5388af3','addColumn tableName=FED_USER_CONSENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('20.0.0-12964-supported-dbs','keycloak','META-INF/jpa-changelog-20.0.0.xml','2026-11-09 17:06:26',109,'EXECUTED','9:f2e1331a71e0aa85e5608fe42f7f681c','createIndex indexName=IDX_GROUP_ATT_BY_NAME_VALUE, tableName=GROUP_ATTRIBUTE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('20.0.0-12964-supported-dbs-edb-migration','keycloak','META-INF/jpa-changelog-20.0.0.xml','2026-11-09 17:06:26',110,'MARK_RAN','9:a6b18a8e38062df5793edbe064f4aecd','dropIndex indexName=IDX_GROUP_ATT_BY_NAME_VALUE, tableName=GROUP_ATTRIBUTE; createIndex indexName=IDX_GROUP_ATT_BY_NAME_VALUE, tableName=GROUP_ATTRIBUTE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('20.0.0-12964-unsupported-dbs','keycloak','META-INF/jpa-changelog-20.0.0.xml','2026-11-09 17:06:26',111,'MARK_RAN','9:1a6fcaa85e20bdeae0a9ce49b41946a5','createIndex indexName=IDX_GROUP_ATT_BY_NAME_VALUE, tableName=GROUP_ATTRIBUTE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('21.0.2-17277','keycloak','META-INF/jpa-changelog-21.0.2.xml','2026-11-09 17:06:26',115,'EXECUTED','9:7ee1f7a3fb8f5588f171fb9a6ab623c0','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('21.1.0-19404','keycloak','META-INF/jpa-changelog-21.1.0.xml','2026-11-09 17:06:26',116,'EXECUTED','9:3d7e830b52f33676b9d64f7f2b2ea634','modifyDataType columnName=DECISION_STRATEGY, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=LOGIC, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=POLICY_ENFORCE_MODE, tableName=RESOURCE_SERVER','',NULL,'4.33.0',NULL,NULL,'4211565042'),('21.1.0-19404-2','keycloak','META-INF/jpa-changelog-21.1.0.xml','2026-11-09 17:06:26',117,'MARK_RAN','9:627d032e3ef2c06c0e1f73d2ae25c26c','addColumn tableName=RESOURCE_SERVER_POLICY; update tableName=RESOURCE_SERVER_POLICY; dropColumn columnName=DECISION_STRATEGY, tableName=RESOURCE_SERVER_POLICY; renameColumn newColumnName=DECISION_STRATEGY, oldColumnName=DECISION_STRATEGY_NEW, tabl...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('22.0.0-17484-updated','keycloak','META-INF/jpa-changelog-22.0.0.xml','2026-11-09 17:06:26',118,'EXECUTED','9:90af0bfd30cafc17b9f4d6eccd92b8b3','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('22.0.5-24031','keycloak','META-INF/jpa-changelog-22.0.0.xml','2026-11-09 17:06:26',119,'MARK_RAN','9:a60d2d7b315ec2d3eba9e2f145f9df28','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('23.0.0-12062','keycloak','META-INF/jpa-changelog-23.0.0.xml','2026-11-09 17:06:26',120,'EXECUTED','9:2168fbe728fec46ae9baf15bf80927b8','addColumn tableName=COMPONENT_CONFIG; update tableName=COMPONENT_CONFIG; dropColumn columnName=VALUE, tableName=COMPONENT_CONFIG; renameColumn newColumnName=VALUE, oldColumnName=VALUE_NEW, tableName=COMPONENT_CONFIG','',NULL,'4.33.0',NULL,NULL,'4211565042'),('23.0.0-17258','keycloak','META-INF/jpa-changelog-23.0.0.xml','2026-11-09 17:06:26',121,'EXECUTED','9:36506d679a83bbfda85a27ea1864dca8','addColumn tableName=EVENT_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('24.0.0-26618-drop-index-if-present','keycloak','META-INF/jpa-changelog-24.0.0.xml','2026-11-09 17:06:26',124,'MARK_RAN','9:04baaf56c116ed19951cbc2cca584022','dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('24.0.0-26618-edb-migration','keycloak','META-INF/jpa-changelog-24.0.0.xml','2026-11-09 17:06:26',126,'MARK_RAN','9:2f684b29d414cd47efe3a3599f390741','dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES; createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('24.0.0-26618-reindex','keycloak','META-INF/jpa-changelog-24.0.0.xml','2026-11-09 17:06:26',125,'EXECUTED','9:bd2bd0fc7768cf0845ac96a8786fa735','createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('24.0.0-9758','keycloak','META-INF/jpa-changelog-24.0.0.xml','2026-11-09 17:06:26',122,'EXECUTED','9:502c557a5189f600f0f445a9b49ebbce','addColumn tableName=USER_ATTRIBUTE; addColumn tableName=FED_USER_ATTRIBUTE; createIndex indexName=USER_ATTR_LONG_VALUES, tableName=USER_ATTRIBUTE; createIndex indexName=FED_USER_ATTR_LONG_VALUES, tableName=FED_USER_ATTRIBUTE; createIndex indexName...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('24.0.0-9758-2','keycloak','META-INF/jpa-changelog-24.0.0.xml','2026-11-09 17:06:26',123,'EXECUTED','9:bf0fdee10afdf597a987adbf291db7b2','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('24.0.2-27228','keycloak','META-INF/jpa-changelog-24.0.2.xml','2026-11-09 17:06:26',127,'EXECUTED','9:eaee11f6b8aa25d2cc6a84fb86fc6238','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('24.0.2-27967-drop-index-if-present','keycloak','META-INF/jpa-changelog-24.0.2.xml','2026-11-09 17:06:26',128,'MARK_RAN','9:04baaf56c116ed19951cbc2cca584022','dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('24.0.2-27967-reindex','keycloak','META-INF/jpa-changelog-24.0.2.xml','2026-11-09 17:06:26',129,'MARK_RAN','9:d3d977031d431db16e2c181ce49d73e9','createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-28265-index-2-mysql','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',136,'EXECUTED','9:b7ef76036d3126bb83c2423bf4d449d6','createIndex indexName=IDX_OFFLINE_USS_BY_BROKER_SESSION_ID, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-28265-index-2-not-mysql','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',137,'MARK_RAN','9:23396cf51ab8bc1ae6f0cac7f9f6fcf7','createIndex indexName=IDX_OFFLINE_USS_BY_BROKER_SESSION_ID, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-28265-index-cleanup-css-preload','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',135,'EXECUTED','9:5411d2fb2891d3e8d63ddb55dfa3c0c9','dropIndex indexName=IDX_OFFLINE_CSS_PRELOAD, tableName=OFFLINE_CLIENT_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-28265-index-cleanup-uss-by-usersess','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',134,'EXECUTED','9:6eee220d024e38e89c799417ec33667f','dropIndex indexName=IDX_OFFLINE_USS_BY_USERSESS, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-28265-index-cleanup-uss-createdon','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',132,'EXECUTED','9:78ab4fc129ed5e8265dbcc3485fba92f','dropIndex indexName=IDX_OFFLINE_USS_CREATEDON, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-28265-index-cleanup-uss-preload','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',133,'EXECUTED','9:de5f7c1f7e10994ed8b62e621d20eaab','dropIndex indexName=IDX_OFFLINE_USS_PRELOAD, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-28265-index-creation','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',131,'EXECUTED','9:3e96709818458ae49f3c679ae58d263a','createIndex indexName=IDX_OFFLINE_USS_BY_LAST_SESSION_REFRESH, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-28265-tables','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',130,'EXECUTED','9:deda2df035df23388af95bbd36c17cef','addColumn tableName=OFFLINE_USER_SESSION; addColumn tableName=OFFLINE_CLIENT_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-28861-index-creation','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',142,'EXECUTED','9:b9acb58ac958d9ada0fe12a5d4794ab1','createIndex indexName=IDX_PERM_TICKET_REQUESTER, tableName=RESOURCE_SERVER_PERM_TICKET; createIndex indexName=IDX_PERM_TICKET_OWNER, tableName=RESOURCE_SERVER_PERM_TICKET','',NULL,'4.33.0',NULL,NULL,'4211565042'),('25.0.0-org','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',138,'EXECUTED','9:5c859965c2c9b9c72136c360649af157','createTable tableName=ORG; addUniqueConstraint constraintName=UK_ORG_NAME, tableName=ORG; addUniqueConstraint constraintName=UK_ORG_GROUP, tableName=ORG; createTable tableName=ORG_DOMAIN','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.0.0-32583-drop-redundant-index-on-client-session','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:27',150,'EXECUTED','9:24972d83bf27317a055d234187bb4af9','dropIndex indexName=IDX_US_SESS_ID_ON_CL_SESS, tableName=OFFLINE_CLIENT_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.0.0-33201-org-redirect-url','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:27',152,'EXECUTED','9:4d0e22b0ac68ebe9794fa9cb752ea660','addColumn tableName=ORG','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.0.0-idps-for-login','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:27',149,'EXECUTED','9:51f5fffadf986983d4bd59582c6c1604','addColumn tableName=IDENTITY_PROVIDER; createIndex indexName=IDX_IDP_REALM_ORG, tableName=IDENTITY_PROVIDER; createIndex indexName=IDX_IDP_FOR_LOGIN, tableName=IDENTITY_PROVIDER; customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.0.0-org-alias','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:26',143,'EXECUTED','9:6ef7d63e4412b3c2d66ed179159886a4','addColumn tableName=ORG; update tableName=ORG; addNotNullConstraint columnName=ALIAS, tableName=ORG; addUniqueConstraint constraintName=UK_ORG_ALIAS, tableName=ORG','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.0.0-org-group','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:26',144,'EXECUTED','9:da8e8087d80ef2ace4f89d8c5b9ca223','addColumn tableName=KEYCLOAK_GROUP; update tableName=KEYCLOAK_GROUP; addNotNullConstraint columnName=TYPE, tableName=KEYCLOAK_GROUP; customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.0.0-org-group-membership','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:26',146,'EXECUTED','9:a6ace2ce583a421d89b01ba2a28dc2d4','addColumn tableName=USER_GROUP_MEMBERSHIP; update tableName=USER_GROUP_MEMBERSHIP; addNotNullConstraint columnName=MEMBERSHIP_TYPE, tableName=USER_GROUP_MEMBERSHIP','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.0.0-org-indexes','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:26',145,'EXECUTED','9:79b05dcd610a8c7f25ec05135eec0857','createIndex indexName=IDX_ORG_DOMAIN_ORG_ID, tableName=ORG_DOMAIN','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.0.0.32582-remove-tables-user-session-user-session-note-and-client-session','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:27',151,'EXECUTED','9:febdc0f47f2ed241c59e60f58c3ceea5','dropTable tableName=CLIENT_SESSION_ROLE; dropTable tableName=CLIENT_SESSION_NOTE; dropTable tableName=CLIENT_SESSION_PROT_MAPPER; dropTable tableName=CLIENT_SESSION_AUTH_STATUS; dropTable tableName=CLIENT_USER_SESSION_NOTE; dropTable tableName=CLI...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.1.0-34013','keycloak','META-INF/jpa-changelog-26.1.0.xml','2026-11-09 17:06:27',154,'EXECUTED','9:e6b686a15759aef99a6d758a5c4c6a26','addColumn tableName=ADMIN_EVENT_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.1.0-34380','keycloak','META-INF/jpa-changelog-26.1.0.xml','2026-11-09 17:06:27',155,'EXECUTED','9:ac8b9edb7c2b6c17a1c7a11fcf5ccf01','dropTable tableName=USERNAME_LOGIN_FAILURE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.2.0-26106','keycloak','META-INF/jpa-changelog-26.2.0.xml','2026-11-09 17:06:27',157,'EXECUTED','9:b5877d5dab7d10ff3a9d209d7beb6680','addColumn tableName=CREDENTIAL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.2.0-36750','keycloak','META-INF/jpa-changelog-26.2.0.xml','2026-11-09 17:06:27',156,'EXECUTED','9:b49ce951c22f7eb16480ff085640a33a','createTable tableName=SERVER_CONFIG','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.2.6-39866-duplicate','keycloak','META-INF/jpa-changelog-26.2.6.xml','2026-11-09 17:06:27',158,'EXECUTED','9:1dc67ccee24f30331db2cba4f372e40e','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.2.6-39866-uk','keycloak','META-INF/jpa-changelog-26.2.6.xml','2026-11-09 17:06:27',159,'EXECUTED','9:b70b76f47210cf0a5f4ef0e219eac7cd','addUniqueConstraint constraintName=UK_MIGRATION_VERSION, tableName=MIGRATION_MODEL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.2.6-40088-duplicate','keycloak','META-INF/jpa-changelog-26.2.6.xml','2026-11-09 17:06:27',160,'EXECUTED','9:cc7e02ed69ab31979afb1982f9670e8f','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.2.6-40088-uk','keycloak','META-INF/jpa-changelog-26.2.6.xml','2026-11-09 17:06:27',161,'EXECUTED','9:5bb848128da7bc4595cc507383325241','addUniqueConstraint constraintName=UK_MIGRATION_UPDATE_TIME, tableName=MIGRATION_MODEL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.3.0-groups-description','keycloak','META-INF/jpa-changelog-26.3.0.xml','2026-11-09 17:06:27',162,'EXECUTED','9:e1a3c05574326fb5b246b73b9a4c4d49','addColumn tableName=KEYCLOAK_GROUP','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.4.0-40933-saml-encryption-attributes','keycloak','META-INF/jpa-changelog-26.4.0.xml','2026-11-09 17:06:27',163,'EXECUTED','9:7e9eaba362ca105efdda202303a4fe49','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.4.0-51321','keycloak','META-INF/jpa-changelog-26.4.0.xml','2026-11-09 17:06:27',164,'EXECUTED','9:34bab2bc56f75ffd7e347c580874e306','createIndex indexName=IDX_EVENT_ENTITY_USER_ID_TYPE, tableName=EVENT_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-add-remember-me','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',172,'EXECUTED','9:a7273ea8b21bd2f674c9c49141999f05','addColumn tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-add-sess-create-idx','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',174,'EXECUTED','9:aaee09e23a4d8468fbc5c51b7b314c58','createIndex indexName=IDX_USER_SESSION_EXPIRATION_LAST_REFRESH, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-add-sess-refresh-idx','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',173,'EXECUTED','9:ce49383d317ccbcd3434d1f21172b0b7','createIndex indexName=IDX_USER_SESSION_EXPIRATION_CREATED, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-drop-sess-refresh-idx','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',175,'EXECUTED','9:f0082210b6ccbbaf81287c27aa23753c','dropIndex indexName=IDX_OFFLINE_USS_BY_LAST_SESSION_REFRESH, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-idp-config-allow-null','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',169,'EXECUTED','9:b667fb087874303b324c1af7fae4f606','dropDefaultValue columnName=TRUST_EMAIL, tableName=IDENTITY_PROVIDER; dropNotNullConstraint columnName=TRUST_EMAIL, tableName=IDENTITY_PROVIDER; dropNotNullConstraint columnName=STORE_TOKEN, tableName=IDENTITY_PROVIDER; dropDefaultValue columnName...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-idp-config-allow-null-fixed-create-mssql-index','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',170,'MARK_RAN','9:dcbbb24c151c3b0b59f12fede23cc94d','createIndex indexName=IDX_IDP_FOR_LOGIN, tableName=IDENTITY_PROVIDER','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-idp-config-allow-null-fixed-drop-mssql-index','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',168,'MARK_RAN','9:50c51d2c98cd1d624eb1c485c3cf1f75','dropIndex indexName=IDX_IDP_FOR_LOGIN, tableName=IDENTITY_PROVIDER','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-index-offline-css-by-client','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',166,'EXECUTED','9:680b59ca7854fa5b77a303301bb2a941','createIndex indexName=IDX_OFFLINE_CSS_BY_CLIENT, tableName=OFFLINE_CLIENT_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-index-offline-css-by-client-storage-provider','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',167,'EXECUTED','9:809bc160e2bc92f9c28eea39db323ae2','createIndex indexName=IDX_OFFLINE_CSS_BY_CLIENT_STORAGE_PROVIDER, tableName=OFFLINE_CLIENT_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-invitations-table-fixed2','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',177,'EXECUTED','9:322cb11fc03181903dcd67a54f8b3cf0','createTable tableName=ORG_INVITATION; addForeignKeyConstraint baseTableName=ORG_INVITATION, constraintName=FK_ORG_INVITATION_ORG, referencedTableName=ORG; createIndex indexName=IDX_ORG_INVITATION_ORG_ID, tableName=ORG_INVITATION; createIndex index...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-mysql-mariadb-default-charset-collation','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',176,'EXECUTED','9:1b383fa60d2db0a8952b365e725f9d16','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.5.0-remove-workflow-provider-id-column','keycloak','META-INF/jpa-changelog-26.5.0.xml','2026-11-09 17:06:27',171,'EXECUTED','9:d8eeb324484d45e946d03b953e168b21','dropIndex indexName=IDX_WORKFLOW_STATE_PROVIDER, tableName=WORKFLOW_STATE; createIndex indexName=IDX_WORKFLOW_STATE_PROVIDER, tableName=WORKFLOW_STATE; dropColumn columnName=WORKFLOW_PROVIDER_ID, tableName=WORKFLOW_STATE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-43829-user-created-timestamp-index','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:28',187,'EXECUTED','9:f2531a49b8bb21a7a97966d88fd1a411','createIndex indexName=IDX_USER_CREATED_TIMESTAMP, tableName=USER_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-44424-create-realm-in-client-session','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:28',182,'EXECUTED','9:77dbbc72d943e98cfe472ba8cc56a31c','addColumn tableName=OFFLINE_CLIENT_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-44424-idx-css-realm-and-clients','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:28',184,'EXECUTED','9:a093877fff41185ac24103be80e00968','createIndex indexName=IDX_OFFLINE_CSS_BY_CLIENT_AND_REALM, tableName=OFFLINE_CLIENT_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-44424-index-css-user-session-and-offline','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:28',181,'EXECUTED','9:a704d8598df241a3fd3cb91b6ab4b2d4','createIndex indexName=IDX_OFFLINE_CSS_BY_USER_SESSION_AND_OFFLINE, tableName=OFFLINE_CLIENT_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-44424-set-realm-in-client-session','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:28',183,'EXECUTED','9:3964a3148d32a55ef81126e23cdf6721','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-45009-broker-link-identity-provider','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:27',179,'EXECUTED','9:7d9a0253c9de7be754efef8bba4265bd','createIndex indexName=IDX_BROKER_LINK_IDENTITY_PROVIDER, tableName=BROKER_LINK','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-45009-broker-link-user-id','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:27',178,'EXECUTED','9:05026bbbc8d2ead5afcbda2f5fdf3a2b','createIndex indexName=IDX_BROKER_LINK_USER_ID, tableName=BROKER_LINK','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-48716-create-mssql-idp-index','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:28',188,'MARK_RAN','9:dcbbb24c151c3b0b59f12fede23cc94d','createIndex indexName=IDX_IDP_FOR_LOGIN, tableName=IDENTITY_PROVIDER','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-add-last-modified-timestamp-user','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:28',185,'EXECUTED','9:8aa583d2cdd9e913dff42fecd626c560','addColumn tableName=USER_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-add-timestamps-group','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:28',186,'EXECUTED','9:4363d45dc25105a3fc5db9ff6936b0a9','addColumn tableName=KEYCLOAK_GROUP','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.6.0-org-group-relationship','keycloak','META-INF/jpa-changelog-26.6.0.xml','2026-11-09 17:06:28',180,'EXECUTED','9:05685853fba030f53548ac6bf23245e3','addColumn tableName=KEYCLOAK_GROUP; addForeignKeyConstraint baseTableName=KEYCLOAK_GROUP, constraintName=FK_GROUP_ORGANIZATION, referencedTableName=ORG; createIndex indexName=IDX_GROUP_ORG_ID, tableName=KEYCLOAK_GROUP','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-45292-realm-display-name-add-column','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',190,'EXECUTED','9:1de8c7824ce4fd7c739db6195f42be21','addColumn tableName=REALM','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-45292-realm-display-name-migrate-data','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',191,'EXECUTED','9:293096bc554dd51428d1d9882f2de1dd','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-45292-realm-display-name-remove-attribute','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',192,'EXECUTED','9:a08357e3b0908c09d478e692cf82f865','delete tableName=REALM_ATTRIBUTE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-46204-issued-ver-credential-table','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',197,'EXECUTED','9:4918c6f68ba90ce417f1aaa031013168','createTable tableName=ISSUED_VER_CREDENTIAL; addPrimaryKey constraintName=PK_ISSUED_VER_CREDENTIAL, tableName=ISSUED_VER_CREDENTIAL; addForeignKeyConstraint baseTableName=ISSUED_VER_CREDENTIAL, constraintName=FK_ISSUED_VER_CREDENTIAL_USER, referen...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-50970','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:29',211,'EXECUTED','9:82981762d25248a32ebfba9f02cee332','createIndex indexName=IDX_WORKFLOW_STATE_SCHEDULED, tableName=WORKFLOW_STATE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-9686-dynamic-scopes-consent','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',196,'EXECUTED','9:fb689bc3ff64e174d6319014b38876f1','addColumn tableName=USER_CONSENT_CLIENT_SCOPE; dropPrimaryKey constraintName=CONSTRAINT_GRNTCSNT_CLSC_PM, tableName=USER_CONSENT_CLIENT_SCOPE; addPrimaryKey constraintName=CONSTRAINT_GRNTCSNT_CLSC_PM, tableName=USER_CONSENT_CLIENT_SCOPE; addColumn...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-add-last-modified-timestamp-client','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:29',209,'EXECUTED','9:bae67d2faa5438ee35adfbb20a53c3c6','addColumn tableName=CLIENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-add-timestamps-client','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:29',208,'EXECUTED','9:df5324c82398b446690b206c07649d40','addColumn tableName=CLIENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-cluster-event','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:29',210,'EXECUTED','9:556b201eb9c378fa05d5bf22ec9c8dcf','createTable tableName=CLUSTER_EVENT; addPrimaryKey constraintName=PK_CLUSTER_EVENT, tableName=CLUSTER_EVENT; createIndex indexName=IDX_CLUSTER_EVENT_TARGET, tableName=CLUSTER_EVENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-federated-issued-ver-credential','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',200,'EXECUTED','9:3d610f5527879623a0d2362e64fa667f','createTable tableName=FED_ISSUED_VER_CREDENTIAL; addForeignKeyConstraint baseTableName=FED_ISSUED_VER_CREDENTIAL, constraintName=FK_FED_ISSUED_VC_VER_CRED, referencedTableName=FED_USER_VER_CREDENTIAL; createIndex indexName=IDX_FED_ISSUED_VC_USER, ...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-federated-verifiable-credentials-1','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',194,'EXECUTED','9:49092fa73b1c2b3afca48d91b8111c65','createTable tableName=FED_USER_VER_CREDENTIAL; addUniqueConstraint constraintName=UK_FED_USER_VC, tableName=FED_USER_VER_CREDENTIAL; createIndex indexName=IDX_FED_USER_VC_REALM_USER, tableName=FED_USER_VER_CREDENTIAL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-issued-ver-credential-expires-at-index','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',198,'EXECUTED','9:ab9e4c0c9f21d9217ffe52968a3cf732','createIndex indexName=IDX_ISSUED_VER_CREDENTIAL_EXPIRES_AT, tableName=ISSUED_VER_CREDENTIAL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-issued-ver-credential-vc-id-index','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',199,'EXECUTED','9:1c9b18926e48b4b66d0341400bd13834','createIndex indexName=IDX_ISSUED_VER_CREDENTIAL_VC, tableName=ISSUED_VER_CREDENTIAL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-jdbcping-timestamp','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',189,'EXECUTED','9:9a91f62e494bd013594e007b74d01638','addColumn tableName=JGROUPS_PING','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-login-failure-index','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:29',207,'EXECUTED','9:f554afc6ad14784c99f6ad8811ac30ec','createIndex indexName=IDX_LOGIN_FAILURE_EXPIRE, tableName=LOGIN_FAILURE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-login-failure-table','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:29',206,'EXECUTED','9:671b50f88904b24ceb02463dd2d0c045','createTable tableName=LOGIN_FAILURE; addPrimaryKey constraintName=PK_LOGIN_FAILURE, tableName=LOGIN_FAILURE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-outbox','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',195,'EXECUTED','9:338b2743ca1be95f895d8f9b0cbe7b55','createTable tableName=OUTBOX_ENTRY; addUniqueConstraint constraintName=UC_OUTBOX_KIND_OWNER_CORRELATION, tableName=OUTBOX_ENTRY; createIndex indexName=IDX_OUTBOX_DRAIN, tableName=OUTBOX_ENTRY; createIndex indexName=IDX_OUTBOX_REALM, tableName=OUTB...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-persistent-auth-session-root-index','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',202,'EXECUTED','9:3090cd11d2dfeb5df754f41c0ffa35d7','createIndex indexName=IDX_ROOT_AUTH_SESSION_REALM, tableName=ROOT_AUTH_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-persistent-auth-session-root-table','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',201,'EXECUTED','9:ad622d5eebdf468747a0d08d2367a68e','createTable tableName=ROOT_AUTH_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-persistent-auth-session-table','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',203,'EXECUTED','9:609b8a172e43f617bb8920efd2b9ae5f','createTable tableName=AUTH_SESSION; addPrimaryKey constraintName=PK_AUTH_SESSION, tableName=AUTH_SESSION; addForeignKeyConstraint baseTableName=AUTH_SESSION, constraintName=FK_AUTH_SESSION_ROOT, referencedTableName=ROOT_AUTH_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-single-use-object-index','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',205,'EXECUTED','9:b2ad66c013f48dc131ce109eface7fa5','createIndex indexName=IDX_SINGLE_USE_OBJ_EXPIRE, tableName=SINGLE_USE_OBJECT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-single-use-object-table','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',204,'EXECUTED','9:22bc4eb8e456b3b7be2808e457a44cb7','createTable tableName=SINGLE_USE_OBJECT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.7.0-verifiable-credential','keycloak','META-INF/jpa-changelog-26.7.0.xml','2026-11-09 17:06:28',193,'EXECUTED','9:68d8df23794085e79ba08b5046cba31d','createTable tableName=USER_VER_CREDENTIAL; addPrimaryKey constraintName=CONSTRAINT_VCRED_PM, tableName=USER_VER_CREDENTIAL; addForeignKeyConstraint baseTableName=USER_VER_CREDENTIAL, constraintName=FK_VCRED_USER, referencedTableName=USER_ENTITY; a...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-51851-add-bucketed-expiration-idx-created','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',217,'EXECUTED','9:f174e4939ae2b6e20003fbe10776d3fe','createIndex indexName=IDX_USER_SESSION_EXPIRATION_CREATED, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-51851-add-session-bucket','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',213,'EXECUTED','9:aec230951f35c974d78dd1f294df15a5','addColumn tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-51851-drop-old-expiration-idx-created','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',215,'EXECUTED','9:0273f3da4167a41778eef56284bf1e9b','dropIndex indexName=IDX_USER_SESSION_EXPIRATION_CREATED, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-51851-drop-old-expiration-idx-last-refresh','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',216,'EXECUTED','9:fea923eeda0c0ff06e2006b46c49bb3f','dropIndex indexName=IDX_USER_SESSION_EXPIRATION_LAST_REFRESH, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-51854-add-filtered-broker-session-idx','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',221,'MARK_RAN','9:23396cf51ab8bc1ae6f0cac7f9f6fcf7','createIndex indexName=IDX_OFFLINE_USS_BY_BROKER_SESSION_ID, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-51854-drop-broker-session-idx','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',220,'MARK_RAN','9:e816715f16e00f007f713bce752beebb','dropIndex indexName=IDX_OFFLINE_USS_BY_BROKER_SESSION_ID, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-51854-drop-css-user-session-offline-idx','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',219,'EXECUTED','9:57c23f6dd89e48f0b1fe2fa8482c36a7','dropIndex indexName=IDX_OFFLINE_CSS_BY_USER_SESSION_AND_OFFLINE, tableName=OFFLINE_CLIENT_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-51900-51851-add-bucketed-and-coarse-expiration-idx-last-refresh','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',218,'EXECUTED','9:095cf7bc0be9e5ed960134103d237cdb','createIndex indexName=IDX_USER_SESSION_EXPIRATION_LAST_REFRESH, tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-51900-add-last-session-refresh-coarse','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',214,'EXECUTED','9:5fd2333a98d3ae004bdf4bf0b356cd88','addColumn tableName=OFFLINE_USER_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-53211-add-bucketed-root-auth-session-idx','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',226,'EXECUTED','9:98933a08c7e98f2124c5438d5ec2a52b','createIndex indexName=IDX_ROOT_AUTH_SESSION_REALM, tableName=ROOT_AUTH_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-53211-add-root-auth-session-bucket','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',222,'EXECUTED','9:cc5ff3f556fe1fc5348cdaeee7040585','addColumn tableName=ROOT_AUTH_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-53211-add-root-auth-session-created-on','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',223,'EXECUTED','9:acf55770b549ccbfb5990780799be30f','addColumn tableName=ROOT_AUTH_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-53211-add-root-auth-session-timestamp-coarse','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',224,'EXECUTED','9:bd48e1f4aa197f804aef55931031ecbd','addColumn tableName=ROOT_AUTH_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-53211-drop-old-root-auth-session-idx','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',225,'EXECUTED','9:f10e6cd0afa4befe76d8161aab680d14','dropIndex indexName=IDX_ROOT_AUTH_SESSION_REALM, tableName=ROOT_AUTH_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-auth-session-auth-user-id-index','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',212,'EXECUTED','9:9d39f9ace96248659e332a25be722f5a','createIndex indexName=IDX_AUTH_SESSION_AUTH_USER_ID, tableName=AUTH_SESSION','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-backfill-group-org-id','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',237,'EXECUTED','9:c834da04f981e7198c7b6298f409f3c7','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-create-org-identity-provider','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',232,'EXECUTED','9:8cdd68d8fbbbb2e1a1d09f7e09892492','createTable tableName=ORG_IDENTITY_PROVIDER; addPrimaryKey constraintName=PK_ORG_IDP, tableName=ORG_IDENTITY_PROVIDER; addForeignKeyConstraint baseTableName=ORG_IDENTITY_PROVIDER, constraintName=FK_ORG_IDP_ORG, referencedTableName=ORG; addForeignK...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-drop-idp-organization-id','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',236,'EXECUTED','9:f1111108b2183ca31c2a74cb1b3494e2','dropIndex indexName=IDX_IDP_REALM_ORG, tableName=IDENTITY_PROVIDER; dropIndex indexName=IDX_IDP_FOR_LOGIN, tableName=IDENTITY_PROVIDER; dropColumn columnName=ORGANIZATION_ID, tableName=IDENTITY_PROVIDER; createIndex indexName=IDX_IDP_FOR_LOGIN, ta...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-idp-mapper-organization-id','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',235,'EXECUTED','9:665accb97ce0a8e0111e8ff57aa93467','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-org-domain-add-idp-columns','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',230,'EXECUTED','9:f40909058fb66836a9c1fa8061dec9f9','addColumn tableName=ORG_DOMAIN','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-org-domain-add-idp-fk','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',234,'EXECUTED','9:ab74c0d43b09017a43b7814e8232765b','addForeignKeyConstraint baseTableName=ORG_DOMAIN, constraintName=FK_ORG_DOMAIN_IDP, referencedTableName=IDENTITY_PROVIDER; createIndex indexName=IDX_ORG_DOMAIN_IDP_ID, tableName=ORG_DOMAIN','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-org-domain-add-org-fk','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',231,'EXECUTED','9:2bee6a398cef692c05ec4c9f78a9cd94','addForeignKeyConstraint baseTableName=ORG_DOMAIN, constraintName=FK_ORG_DOMAIN_ORG, referencedTableName=ORG','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-org-domain-add-realm-id','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',227,'EXECUTED','9:1495524d8e111590a9561921445e0bf2','addColumn tableName=ORG_DOMAIN','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-org-domain-populate-realm-id','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',228,'EXECUTED','9:12ca3d104545ae937c26dcb1a518c93c','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-org-domain-realm-id-not-null','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',229,'EXECUTED','9:b9354aa858afdd63abc3c4cb8d94d0c3','addNotNullConstraint columnName=REALM_ID, tableName=ORG_DOMAIN; addUniqueConstraint constraintName=UK_ORG_DOMAIN_REALM_NAME, tableName=ORG_DOMAIN; createIndex indexName=IDX_ORG_DOMAIN_REALM, tableName=ORG_DOMAIN','',NULL,'4.33.0',NULL,NULL,'4211565042'),('26.8.0-org-idp-and-domain-routing-migration','keycloak','META-INF/jpa-changelog-26.8.0.xml','2026-11-09 17:06:29',233,'EXECUTED','9:833e203db6b2bcaa07f38b286ecad308','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('29399-jdbc-ping-default','keycloak','META-INF/jpa-changelog-26.1.0.xml','2026-11-09 17:06:27',153,'EXECUTED','9:007dbe99d7203fca403b89d4edfdf21e','createTable tableName=JGROUPS_PING; addPrimaryKey constraintName=CONSTRAINT_JGROUPS_PING, tableName=JGROUPS_PING','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.0.0','bburke@redhat.com','META-INF/jpa-changelog-3.0.0.xml','2026-11-09 17:06:20',39,'EXECUTED','9:132a67499ba24bcc54fb5cbdcfe7e4c0','addColumn tableName=IDENTITY_PROVIDER','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.2.0-fix','keycloak','META-INF/jpa-changelog-3.2.0.xml','2026-11-09 17:06:20',40,'MARK_RAN','9:938f894c032f5430f2b0fafb1a243462','addNotNullConstraint columnName=REALM_ID, tableName=CLIENT_INITIAL_ACCESS','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.2.0-fix-offline-sessions','hmlnarik','META-INF/jpa-changelog-3.2.0.xml','2026-11-09 17:06:21',42,'EXECUTED','9:fc86359c079781adc577c5a217e4d04c','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.2.0-fix-with-keycloak-5416','keycloak','META-INF/jpa-changelog-3.2.0.xml','2026-11-09 17:06:20',41,'MARK_RAN','9:845c332ff1874dc5d35974b0babf3006','dropIndex indexName=IDX_CLIENT_INIT_ACC_REALM, tableName=CLIENT_INITIAL_ACCESS; addNotNullConstraint columnName=REALM_ID, tableName=CLIENT_INITIAL_ACCESS; createIndex indexName=IDX_CLIENT_INIT_ACC_REALM, tableName=CLIENT_INITIAL_ACCESS','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.2.0-fixed','keycloak','META-INF/jpa-changelog-3.2.0.xml','2026-11-09 17:06:21',43,'EXECUTED','9:59a64800e3c0d09b825f8a3b444fa8f4','addColumn tableName=REALM; dropPrimaryKey constraintName=CONSTRAINT_OFFL_CL_SES_PK2, tableName=OFFLINE_CLIENT_SESSION; dropColumn columnName=CLIENT_SESSION_ID, tableName=OFFLINE_CLIENT_SESSION; addPrimaryKey constraintName=CONSTRAINT_OFFL_CL_SES_P...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.3.0','keycloak','META-INF/jpa-changelog-3.3.0.xml','2026-11-09 17:06:21',44,'EXECUTED','9:d48d6da5c6ccf667807f633fe489ce88','addColumn tableName=USER_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.4.0','keycloak','META-INF/jpa-changelog-3.4.0.xml','2026-11-09 17:06:22',50,'EXECUTED','9:cfdd8736332ccdd72c5256ccb42335db','addPrimaryKey constraintName=CONSTRAINT_REALM_DEFAULT_ROLES, tableName=REALM_DEFAULT_ROLES; addPrimaryKey constraintName=CONSTRAINT_COMPOSITE_ROLE, tableName=COMPOSITE_ROLE; addPrimaryKey constraintName=CONSTR_REALM_DEFAULT_GROUPS, tableName=REALM...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.4.0-KEYCLOAK-5230','hmlnarik@redhat.com','META-INF/jpa-changelog-3.4.0.xml','2026-11-09 17:06:23',51,'EXECUTED','9:7c84de3d9bd84d7f077607c1a4dcb714','createIndex indexName=IDX_FU_ATTRIBUTE, tableName=FED_USER_ATTRIBUTE; createIndex indexName=IDX_FU_CONSENT, tableName=FED_USER_CONSENT; createIndex indexName=IDX_FU_CONSENT_RU, tableName=FED_USER_CONSENT; createIndex indexName=IDX_FU_CREDENTIAL, t...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.4.1','psilva@redhat.com','META-INF/jpa-changelog-3.4.1.xml','2026-11-09 17:06:23',52,'EXECUTED','9:5a6bb36cbefb6a9d6928452c0852af2d','modifyDataType columnName=VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.4.2','keycloak','META-INF/jpa-changelog-3.4.2.xml','2026-11-09 17:06:23',53,'EXECUTED','9:8f23e334dbc59f82e0a328373ca6ced0','update tableName=REALM','',NULL,'4.33.0',NULL,NULL,'4211565042'),('3.4.2-KEYCLOAK-5172','mkanis@redhat.com','META-INF/jpa-changelog-3.4.2.xml','2026-11-09 17:06:23',54,'EXECUTED','9:9156214268f09d970cdf0e1564d866af','update tableName=CLIENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('31296-persist-revoked-access-tokens','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:26',147,'EXECUTED','9:64ef94489d42a358e8304b0e245f0ed4','createTable tableName=REVOKED_TOKEN; addPrimaryKey constraintName=CONSTRAINT_RT, tableName=REVOKED_TOKEN','',NULL,'4.33.0',NULL,NULL,'4211565042'),('31725-index-persist-revoked-access-tokens','keycloak','META-INF/jpa-changelog-26.0.0.xml','2026-11-09 17:06:26',148,'EXECUTED','9:b994246ec2bf7c94da881e1d28782c7b','createIndex indexName=IDX_REV_TOKEN_ON_EXPIRE, tableName=REVOKED_TOKEN','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.0.0-CLEANUP-UNUSED-TABLE','bburke@redhat.com','META-INF/jpa-changelog-4.0.0.xml','2026-11-09 17:06:23',56,'EXECUTED','9:229a041fb72d5beac76bb94a5fa709de','dropTable tableName=CLIENT_IDENTITY_PROV_MAPPING','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.0.0-KEYCLOAK-5579-fixed','mposolda@redhat.com','META-INF/jpa-changelog-4.0.0.xml','2026-11-09 17:06:24',58,'EXECUTED','9:139b79bcbbfe903bb1c2d2a4dbf001d9','dropForeignKeyConstraint baseTableName=CLIENT_TEMPLATE_ATTRIBUTES, constraintName=FK_CL_TEMPL_ATTR_TEMPL; renameTable newTableName=CLIENT_SCOPE_ATTRIBUTES, oldTableName=CLIENT_TEMPLATE_ATTRIBUTES; renameColumn newColumnName=SCOPE_ID, oldColumnName...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.0.0-KEYCLOAK-6228','bburke@redhat.com','META-INF/jpa-changelog-4.0.0.xml','2026-11-09 17:06:23',57,'EXECUTED','9:079899dade9c1e683f26b2aa9ca6ff04','dropUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHOGM8UEWRT, tableName=USER_CONSENT; dropNotNullConstraint columnName=CLIENT_ID, tableName=USER_CONSENT; addColumn tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHO...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.0.0-KEYCLOAK-6335','bburke@redhat.com','META-INF/jpa-changelog-4.0.0.xml','2026-11-09 17:06:23',55,'EXECUTED','9:db806613b1ed154826c02610b7dbdf74','createTable tableName=CLIENT_AUTH_FLOW_BINDINGS; addPrimaryKey constraintName=C_CLI_FLOW_BIND, tableName=CLIENT_AUTH_FLOW_BINDINGS','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.2.0-KEYCLOAK-6313','wadahiro@gmail.com','META-INF/jpa-changelog-4.2.0.xml','2026-11-09 17:06:24',63,'EXECUTED','9:92143a6daea0a3f3b8f598c97ce55c3d','addColumn tableName=REQUIRED_ACTION_PROVIDER','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.3.0-KEYCLOAK-7984','wadahiro@gmail.com','META-INF/jpa-changelog-4.3.0.xml','2026-11-09 17:06:24',64,'EXECUTED','9:82bab26a27195d889fb0429003b18f40','update tableName=REQUIRED_ACTION_PROVIDER','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.6.0-KEYCLOAK-7950','psilva@redhat.com','META-INF/jpa-changelog-4.6.0.xml','2026-11-09 17:06:24',65,'EXECUTED','9:e590c88ddc0b38b0ae4249bbfcb5abc3','update tableName=RESOURCE_SERVER_RESOURCE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.6.0-KEYCLOAK-8377','keycloak','META-INF/jpa-changelog-4.6.0.xml','2026-11-09 17:06:24',66,'EXECUTED','9:5c1f475536118dbdc38d5d7977950cc0','createTable tableName=ROLE_ATTRIBUTE; addPrimaryKey constraintName=CONSTRAINT_ROLE_ATTRIBUTE_PK, tableName=ROLE_ATTRIBUTE; addForeignKeyConstraint baseTableName=ROLE_ATTRIBUTE, constraintName=FK_ROLE_ATTRIBUTE_ID, referencedTableName=KEYCLOAK_ROLE...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.6.0-KEYCLOAK-8555','gideonray@gmail.com','META-INF/jpa-changelog-4.6.0.xml','2026-11-09 17:06:24',67,'EXECUTED','9:e7c9f5f9c4d67ccbbcc215440c718a17','createIndex indexName=IDX_COMPONENT_PROVIDER_TYPE, tableName=COMPONENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.7.0-KEYCLOAK-1267','sguilhen@redhat.com','META-INF/jpa-changelog-4.7.0.xml','2026-11-09 17:06:24',68,'EXECUTED','9:88e0bfdda924690d6f4e430c53447dd5','addColumn tableName=REALM','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.7.0-KEYCLOAK-7275','keycloak','META-INF/jpa-changelog-4.7.0.xml','2026-11-09 17:06:24',69,'EXECUTED','9:f53177f137e1c46b6a88c59ec1cb5218','renameColumn newColumnName=CREATED_ON, oldColumnName=LAST_SESSION_REFRESH, tableName=OFFLINE_USER_SESSION; addNotNullConstraint columnName=CREATED_ON, tableName=OFFLINE_USER_SESSION; addColumn tableName=OFFLINE_USER_SESSION; customChange; createIn...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('4.8.0-KEYCLOAK-8835','sguilhen@redhat.com','META-INF/jpa-changelog-4.8.0.xml','2026-11-09 17:06:25',70,'EXECUTED','9:a74d33da4dc42a37ec27121580d1459f','addNotNullConstraint columnName=SSO_MAX_LIFESPAN_REMEMBER_ME, tableName=REALM; addNotNullConstraint columnName=SSO_IDLE_TIMEOUT_REMEMBER_ME, tableName=REALM','',NULL,'4.33.0',NULL,NULL,'4211565042'),('40343-workflow-state-table','keycloak','META-INF/jpa-changelog-26.4.0.xml','2026-11-09 17:06:27',165,'EXECUTED','9:ed3ab4723ceed210e5b5e60ac4562106','createTable tableName=WORKFLOW_STATE; addPrimaryKey constraintName=PK_WORKFLOW_STATE, tableName=WORKFLOW_STATE; addUniqueConstraint constraintName=UQ_WORKFLOW_RESOURCE, tableName=WORKFLOW_STATE; createIndex indexName=IDX_WORKFLOW_STATE_STEP, table...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('8.0.0-adding-credential-columns','keycloak','META-INF/jpa-changelog-8.0.0.xml','2026-11-09 17:06:25',72,'EXECUTED','9:aa072ad090bbba210d8f18781b8cebf4','addColumn tableName=CREDENTIAL; addColumn tableName=FED_USER_CREDENTIAL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('8.0.0-credential-cleanup-fixed','keycloak','META-INF/jpa-changelog-8.0.0.xml','2026-11-09 17:06:25',75,'EXECUTED','9:2b9cc12779be32c5b40e2e67711a218b','dropDefaultValue columnName=COUNTER, tableName=CREDENTIAL; dropDefaultValue columnName=DIGITS, tableName=CREDENTIAL; dropDefaultValue columnName=PERIOD, tableName=CREDENTIAL; dropDefaultValue columnName=ALGORITHM, tableName=CREDENTIAL; dropColumn ...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('8.0.0-resource-tag-support','keycloak','META-INF/jpa-changelog-8.0.0.xml','2026-11-09 17:06:25',76,'EXECUTED','9:91fa186ce7a5af127a2d7a91ee083cc5','addColumn tableName=MIGRATION_MODEL; createIndex indexName=IDX_UPDATE_TIME, tableName=MIGRATION_MODEL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('8.0.0-updating-credential-data-not-oracle-fixed','keycloak','META-INF/jpa-changelog-8.0.0.xml','2026-11-09 17:06:25',73,'EXECUTED','9:1ae6be29bab7c2aa376f6983b932be37','update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=FED_USER_CREDENTIAL; update tableName=FED_USER_CREDENTIAL; update tableName=FED_USER_CREDENTIAL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('8.0.0-updating-credential-data-oracle-fixed','keycloak','META-INF/jpa-changelog-8.0.0.xml','2026-11-09 17:06:25',74,'MARK_RAN','9:14706f286953fc9a25286dbd8fb30d97','update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=FED_USER_CREDENTIAL; update tableName=FED_USER_CREDENTIAL; update tableName=FED_USER_CREDENTIAL','',NULL,'4.33.0',NULL,NULL,'4211565042'),('9.0.0-always-display-client','keycloak','META-INF/jpa-changelog-9.0.0.xml','2026-11-09 17:06:25',77,'EXECUTED','9:6335e5c94e83a2639ccd68dd24e2e5ad','addColumn tableName=CLIENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('9.0.0-drop-constraints-for-column-increase','keycloak','META-INF/jpa-changelog-9.0.0.xml','2026-11-09 17:06:25',78,'MARK_RAN','9:6bdb5658951e028bfe16fa0a8228b530','dropUniqueConstraint constraintName=UK_FRSR6T700S9V50BU18WS5PMT, tableName=RESOURCE_SERVER_PERM_TICKET; dropUniqueConstraint constraintName=UK_FRSR6T700S9V50BU18WS5HA6, tableName=RESOURCE_SERVER_RESOURCE; dropPrimaryKey constraintName=CONSTRAINT_O...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('9.0.0-increase-column-size-federated-fk','keycloak','META-INF/jpa-changelog-9.0.0.xml','2026-11-09 17:06:25',79,'EXECUTED','9:d5bc15a64117ccad481ce8792d4c608f','modifyDataType columnName=CLIENT_ID, tableName=FED_USER_CONSENT; modifyDataType columnName=CLIENT_REALM_CONSTRAINT, tableName=KEYCLOAK_ROLE; modifyDataType columnName=OWNER, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=CLIENT_ID, ta...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('9.0.0-recreate-constraints-after-column-increase','keycloak','META-INF/jpa-changelog-9.0.0.xml','2026-11-09 17:06:25',80,'MARK_RAN','9:077cba51999515f4d3e7ad5619ab592c','addNotNullConstraint columnName=CLIENT_ID, tableName=OFFLINE_CLIENT_SESSION; addNotNullConstraint columnName=OWNER, tableName=RESOURCE_SERVER_PERM_TICKET; addNotNullConstraint columnName=REQUESTER, tableName=RESOURCE_SERVER_PERM_TICKET; addNotNull...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('9.0.1-add-index-to-client.client_id','keycloak','META-INF/jpa-changelog-9.0.1.xml','2026-11-09 17:06:25',81,'EXECUTED','9:be969f08a163bf47c6b9e9ead8ac2afb','createIndex indexName=IDX_CLIENT_ID, tableName=CLIENT','',NULL,'4.33.0',NULL,NULL,'4211565042'),('9.0.1-add-index-to-events','keycloak','META-INF/jpa-changelog-9.0.1.xml','2026-11-09 17:06:25',85,'EXECUTED','9:7d93d602352a30c0c317e6a609b56599','createIndex indexName=IDX_EVENT_TIME, tableName=EVENT_ENTITY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('9.0.1-KEYCLOAK-12579-add-not-null-constraint','keycloak','META-INF/jpa-changelog-9.0.1.xml','2026-11-09 17:06:25',83,'EXECUTED','9:966bda61e46bebf3cc39518fbed52fa7','addNotNullConstraint columnName=PARENT_GROUP, tableName=KEYCLOAK_GROUP','',NULL,'4.33.0',NULL,NULL,'4211565042'),('9.0.1-KEYCLOAK-12579-drop-constraints','keycloak','META-INF/jpa-changelog-9.0.1.xml','2026-11-09 17:06:25',82,'MARK_RAN','9:6d3bb4408ba5a72f39bd8a0b301ec6e3','dropUniqueConstraint constraintName=SIBLING_NAMES, tableName=KEYCLOAK_GROUP','',NULL,'4.33.0',NULL,NULL,'4211565042'),('9.0.1-KEYCLOAK-12579-recreate-constraints','keycloak','META-INF/jpa-changelog-9.0.1.xml','2026-11-09 17:06:25',84,'MARK_RAN','9:8dcac7bdf7378e7d823cdfddebf72fda','addUniqueConstraint constraintName=SIBLING_NAMES, tableName=KEYCLOAK_GROUP','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authn-3.4.0.CR1-refresh-token-max-reuse','glavoie@gmail.com','META-INF/jpa-changelog-authz-3.4.0.CR1.xml','2026-11-09 17:06:22',49,'EXECUTED','9:d198654156881c46bfba39abd7769e69','addColumn tableName=REALM','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-2.0.0','psilva@redhat.com','META-INF/jpa-changelog-authz-2.0.0.xml','2026-11-09 17:06:19',27,'EXECUTED','9:43ed6b0da89ff77206289e87eaa9c024','createTable tableName=RESOURCE_SERVER; addPrimaryKey constraintName=CONSTRAINT_FARS, tableName=RESOURCE_SERVER; addUniqueConstraint constraintName=UK_AU8TT6T700S9V50BU18WS5HA6, tableName=RESOURCE_SERVER; createTable tableName=RESOURCE_SERVER_RESOU...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-2.5.1','psilva@redhat.com','META-INF/jpa-changelog-authz-2.5.1.xml','2026-11-09 17:06:19',28,'EXECUTED','9:44bae577f551b3738740281eceb4ea70','update tableName=RESOURCE_SERVER_POLICY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-3.4.0.CR1-resource-server-pk-change-part1','glavoie@gmail.com','META-INF/jpa-changelog-authz-3.4.0.CR1.xml','2026-11-09 17:06:21',45,'EXECUTED','9:dde36f7973e80d71fceee683bc5d2951','addColumn tableName=RESOURCE_SERVER_POLICY; addColumn tableName=RESOURCE_SERVER_RESOURCE; addColumn tableName=RESOURCE_SERVER_SCOPE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-3.4.0.CR1-resource-server-pk-change-part2-KEYCLOAK-6095','hmlnarik@redhat.com','META-INF/jpa-changelog-authz-3.4.0.CR1.xml','2026-11-09 17:06:21',46,'EXECUTED','9:b855e9b0a406b34fa323235a0cf4f640','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-3.4.0.CR1-resource-server-pk-change-part3-fixed','glavoie@gmail.com','META-INF/jpa-changelog-authz-3.4.0.CR1.xml','2026-11-09 17:06:21',47,'MARK_RAN','9:51abbacd7b416c50c4421a8cabf7927e','dropIndex indexName=IDX_RES_SERV_POL_RES_SERV, tableName=RESOURCE_SERVER_POLICY; dropIndex indexName=IDX_RES_SRV_RES_RES_SRV, tableName=RESOURCE_SERVER_RESOURCE; dropIndex indexName=IDX_RES_SRV_SCOPE_RES_SRV, tableName=RESOURCE_SERVER_SCOPE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-3.4.0.CR1-resource-server-pk-change-part3-fixed-nodropindex','glavoie@gmail.com','META-INF/jpa-changelog-authz-3.4.0.CR1.xml','2026-11-09 17:06:22',48,'EXECUTED','9:bdc99e567b3398bac83263d375aad143','addNotNullConstraint columnName=RESOURCE_SERVER_CLIENT_ID, tableName=RESOURCE_SERVER_POLICY; addNotNullConstraint columnName=RESOURCE_SERVER_CLIENT_ID, tableName=RESOURCE_SERVER_RESOURCE; addNotNullConstraint columnName=RESOURCE_SERVER_CLIENT_ID, ...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-4.0.0.Beta3','psilva@redhat.com','META-INF/jpa-changelog-authz-4.0.0.Beta3.xml','2026-11-09 17:06:24',60,'EXECUTED','9:e0057eac39aa8fc8e09ac6cfa4ae15fe','addColumn tableName=RESOURCE_SERVER_POLICY; addColumn tableName=RESOURCE_SERVER_PERM_TICKET; addForeignKeyConstraint baseTableName=RESOURCE_SERVER_PERM_TICKET, constraintName=FK_FRSRPO2128CX4WNKOG82SSRFY, referencedTableName=RESOURCE_SERVER_POLICY','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-4.0.0.CR1','psilva@redhat.com','META-INF/jpa-changelog-authz-4.0.0.CR1.xml','2026-11-09 17:06:24',59,'EXECUTED','9:b55738ad889860c625ba2bf483495a04','createTable tableName=RESOURCE_SERVER_PERM_TICKET; addPrimaryKey constraintName=CONSTRAINT_FAPMT, tableName=RESOURCE_SERVER_PERM_TICKET; addForeignKeyConstraint baseTableName=RESOURCE_SERVER_PERM_TICKET, constraintName=FK_FRSRHO213XCX4WNKOG82SSPMT...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-4.2.0.Final','mhajas@redhat.com','META-INF/jpa-changelog-authz-4.2.0.Final.xml','2026-11-09 17:06:24',61,'EXECUTED','9:42a33806f3a0443fe0e7feeec821326c','createTable tableName=RESOURCE_URIS; addForeignKeyConstraint baseTableName=RESOURCE_URIS, constraintName=FK_RESOURCE_SERVER_URIS, referencedTableName=RESOURCE_SERVER_RESOURCE; customChange; dropColumn columnName=URI, tableName=RESOURCE_SERVER_RESO...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-4.2.0.Final-KEYCLOAK-9944','hmlnarik@redhat.com','META-INF/jpa-changelog-authz-4.2.0.Final.xml','2026-11-09 17:06:24',62,'EXECUTED','9:9968206fca46eecc1f51db9c024bfe56','addPrimaryKey constraintName=CONSTRAINT_RESOUR_URIS_PK, tableName=RESOURCE_URIS','',NULL,'4.33.0',NULL,NULL,'4211565042'),('authz-7.0.0-KEYCLOAK-10443','psilva@redhat.com','META-INF/jpa-changelog-authz-7.0.0.xml','2026-11-09 17:06:25',71,'EXECUTED','9:fd4ade7b90c3b67fae0bfcfcb42dfb5f','addColumn tableName=RESOURCE_SERVER','',NULL,'4.33.0',NULL,NULL,'4211565042'),('client-attributes-string-accomodation-fixed','keycloak','META-INF/jpa-changelog-20.0.0.xml','2026-11-09 17:06:26',113,'EXECUTED','9:3f332e13e90739ed0c35b0b25b7822ca','addColumn tableName=CLIENT_ATTRIBUTES; update tableName=CLIENT_ATTRIBUTES; dropColumn columnName=VALUE, tableName=CLIENT_ATTRIBUTES; renameColumn newColumnName=VALUE, oldColumnName=VALUE_NEW, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('client-attributes-string-accomodation-fixed-post-create-index','keycloak','META-INF/jpa-changelog-20.0.0.xml','2026-11-09 17:06:26',114,'MARK_RAN','9:bd2bd0fc7768cf0845ac96a8786fa735','createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('client-attributes-string-accomodation-fixed-pre-drop-index','keycloak','META-INF/jpa-changelog-20.0.0.xml','2026-11-09 17:06:26',112,'EXECUTED','9:04baaf56c116ed19951cbc2cca584022','dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('default-roles','keycloak','META-INF/jpa-changelog-13.0.0.xml','2026-11-09 17:06:25',89,'EXECUTED','9:fa8a5b5445e3857f4b010bafb5009957','addColumn tableName=REALM; customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('default-roles-cleanup','keycloak','META-INF/jpa-changelog-13.0.0.xml','2026-11-09 17:06:25',90,'EXECUTED','9:67ac3241df9a8582d591c5ed87125f39','dropTable tableName=REALM_DEFAULT_ROLES; dropTable tableName=CLIENT_DEFAULT_ROLES','',NULL,'4.33.0',NULL,NULL,'4211565042'),('json-string-accomodation-fixed','keycloak','META-INF/jpa-changelog-13.0.0.xml','2026-11-09 17:06:25',96,'EXECUTED','9:e07d2bc0970c348bb06fb63b1f82ddbf','addColumn tableName=REALM_ATTRIBUTE; update tableName=REALM_ATTRIBUTE; dropColumn columnName=VALUE, tableName=REALM_ATTRIBUTE; renameColumn newColumnName=VALUE, oldColumnName=VALUE_NEW, tableName=REALM_ATTRIBUTE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('KEYCLOAK-17267-add-index-to-user-attributes','keycloak','META-INF/jpa-changelog-14.0.0.xml','2026-11-09 17:06:26',102,'EXECUTED','9:0b305d8d1277f3a89a0a53a659ad274c','createIndex indexName=IDX_USER_ATTRIBUTE_NAME, tableName=USER_ATTRIBUTE','',NULL,'4.33.0',NULL,NULL,'4211565042'),('KEYCLOAK-18146-add-saml-art-binding-identifier','keycloak','META-INF/jpa-changelog-14.0.0.xml','2026-11-09 17:06:26',103,'EXECUTED','9:2c374ad2cdfe20e2905a84c8fac48460','customChange','',NULL,'4.33.0',NULL,NULL,'4211565042'),('map-remove-ri','keycloak','META-INF/jpa-changelog-11.0.0.xml','2026-11-09 17:06:25',86,'EXECUTED','9:71c5969e6cdd8d7b6f47cebc86d37627','dropForeignKeyConstraint baseTableName=REALM, constraintName=FK_TRAF444KK6QRKMS7N56AIWQ5Y; dropForeignKeyConstraint baseTableName=KEYCLOAK_ROLE, constraintName=FK_KJHO5LE2C0RAL09FL8CM9WFW9','',NULL,'4.33.0',NULL,NULL,'4211565042'),('map-remove-ri','keycloak','META-INF/jpa-changelog-12.0.0.xml','2026-11-09 17:06:25',87,'EXECUTED','9:a9ba7d47f065f041b7da856a81762021','dropForeignKeyConstraint baseTableName=REALM_DEFAULT_GROUPS, constraintName=FK_DEF_GROUPS_GROUP; dropForeignKeyConstraint baseTableName=REALM_DEFAULT_ROLES, constraintName=FK_H4WPD7W4HSOOLNI3H0SW7BTJE; dropForeignKeyConstraint baseTableName=CLIENT...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('map-remove-ri-13.0.0','keycloak','META-INF/jpa-changelog-13.0.0.xml','2026-11-09 17:06:25',92,'EXECUTED','9:d9be619d94af5a2f5d07b9f003543b91','dropForeignKeyConstraint baseTableName=DEFAULT_CLIENT_SCOPE, constraintName=FK_R_DEF_CLI_SCOPE_SCOPE; dropForeignKeyConstraint baseTableName=CLIENT_SCOPE_CLIENT, constraintName=FK_C_CLI_SCOPE_SCOPE; dropForeignKeyConstraint baseTableName=CLIENT_SC...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('unique-consentuser','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',139,'MARK_RAN','9:5857626a2ea8767e9a6c66bf3a2cb32f','customChange; dropUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHOGM8UEWRT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_LOCAL_CONSENT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_EXTERNAL_CONSENT, tableName=...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('unique-consentuser-edb-migration','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',140,'MARK_RAN','9:5857626a2ea8767e9a6c66bf3a2cb32f','customChange; dropUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHOGM8UEWRT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_LOCAL_CONSENT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_EXTERNAL_CONSENT, tableName=...','',NULL,'4.33.0',NULL,NULL,'4211565042'),('unique-consentuser-mysql','keycloak','META-INF/jpa-changelog-25.0.0.xml','2026-11-09 17:06:26',141,'EXECUTED','9:b79478aad5adaa1bc428e31563f55e8e','customChange; dropUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHOGM8UEWRT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_LOCAL_CONSENT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_EXTERNAL_CONSENT, tableName=...','',NULL,'4.33.0',NULL,NULL,'4211565042');
UNLOCK TABLES;

--
-- Dumping data for table `databasechangeloglock`
--

LOCK TABLES `databasechangeloglock` WRITE;
INSERT INTO `databasechangeloglock` VALUES (1,0,NULL,NULL),(1000,0,NULL,NULL);
UNLOCK TABLES;

--
-- Dumping data for table `default_client_scope`
--

LOCK TABLES `default_client_scope` WRITE;
INSERT INTO `default_client_scope` VALUES ('faaacb96-1668-4dd7-b538-000594f408e6','0b5b5753-25ad-41c5-b2fb-024f036c101a',1),('faaacb96-1668-4dd7-b538-000594f408e6','1fdb82c7-6ab9-4d1f-b608-bd2f525fe810',1),('faaacb96-1668-4dd7-b538-000594f408e6','23dd2041-cb93-488c-9ef0-910909a90987',1),('faaacb96-1668-4dd7-b538-000594f408e6','30671452-f0df-40bc-90c9-91222fc2bec5',0),('faaacb96-1668-4dd7-b538-000594f408e6','349cd61f-65a1-4f1e-9370-de157d8a9920',1),('faaacb96-1668-4dd7-b538-000594f408e6','42d1ea7a-f39d-49c8-8777-7fd6b457e871',1),('faaacb96-1668-4dd7-b538-000594f408e6','4acbebfd-4e12-4551-afc9-6ea3682610a3',0),('faaacb96-1668-4dd7-b538-000594f408e6','5ac886e2-fbb9-44b5-9ff9-dbe4fa973d3f',1),('faaacb96-1668-4dd7-b538-000594f408e6','5f5b905a-4d28-40f1-8350-99dfd37c904e',0),('faaacb96-1668-4dd7-b538-000594f408e6','61f99739-6fce-43f9-958e-f3ea982b6e55',1),('faaacb96-1668-4dd7-b538-000594f408e6','67d5f582-ecc0-42d6-9f65-2c0452d5e397',1),('faaacb96-1668-4dd7-b538-000594f408e6','9be0037a-51a5-4eb3-b14a-24d9135ffd1c',0),('faaacb96-1668-4dd7-b538-000594f408e6','9e94b502-44b3-473d-a357-97ac8014913a',0),('faaacb96-1668-4dd7-b538-000594f408e6','d14d6d0a-565b-48d1-b7d1-de0a879d723a',1);
UNLOCK TABLES;

--
-- Dumping data for table `event_entity`
--

LOCK TABLES `event_entity` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `fed_issued_ver_credential`
--

LOCK TABLES `fed_issued_ver_credential` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `fed_user_attribute`
--

LOCK TABLES `fed_user_attribute` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `fed_user_consent`
--

LOCK TABLES `fed_user_consent` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `fed_user_consent_cl_scope`
--

LOCK TABLES `fed_user_consent_cl_scope` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `fed_user_credential`
--

LOCK TABLES `fed_user_credential` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `fed_user_group_membership`
--

LOCK TABLES `fed_user_group_membership` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `fed_user_required_action`
--

LOCK TABLES `fed_user_required_action` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `fed_user_role_mapping`
--

LOCK TABLES `fed_user_role_mapping` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `fed_user_ver_credential`
--

LOCK TABLES `fed_user_ver_credential` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `federated_identity`
--

LOCK TABLES `federated_identity` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `federated_user`
--

LOCK TABLES `federated_user` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `group_attribute`
--

LOCK TABLES `group_attribute` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `group_role_mapping`
--

LOCK TABLES `group_role_mapping` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `identity_provider`
--

LOCK TABLES `identity_provider` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `identity_provider_config`
--

LOCK TABLES `identity_provider_config` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `identity_provider_mapper`
--

LOCK TABLES `identity_provider_mapper` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `idp_mapper_config`
--

LOCK TABLES `idp_mapper_config` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `issued_ver_credential`
--

LOCK TABLES `issued_ver_credential` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `jgroups_ping`
--

LOCK TABLES `jgroups_ping` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `keycloak_group`
--

LOCK TABLES `keycloak_group` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `keycloak_role`
--

LOCK TABLES `keycloak_role` WRITE;
INSERT INTO `keycloak_role` VALUES ('103e63e0-b7bc-47b0-88ca-c13c11eecb1b','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_query-users}','query-users','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('2dc0db2c-d02d-49ce-b1b6-e57923fd2129','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_view-clients}','view-clients','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('352e2bda-e324-4a7f-83b5-219802c4c320','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_view-realm}','view-realm','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('3a2b8342-ae3f-4ad6-8a4a-c019aa3dab3a','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_create-client}','create-client','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('40d9509c-23b2-4d95-87cd-214e7abb7281','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_view-events}','view-events','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('455d5e7c-72c5-4557-9544-ebcfe8e9a234','faaacb96-1668-4dd7-b538-000594f408e6',0,'${role_offline-access}','offline_access','faaacb96-1668-4dd7-b538-000594f408e6',NULL,NULL),('4e020b36-c21c-4d99-93d2-d1a983060944','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_view-authorization}','view-authorization','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('5046830b-e0fc-41a9-ace4-e7d9a4cd2ad6','262407fa-fb61-433e-bf95-a730e7df9247',1,'${role_read-token}','read-token','faaacb96-1668-4dd7-b538-000594f408e6','262407fa-fb61-433e-bf95-a730e7df9247',NULL),('51fef47e-159b-4675-9b5c-3a3e51dc62fc','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_view-organizations}','view-organizations','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('6cdd393e-7805-46f1-ba1a-af0021753e4f','faaacb96-1668-4dd7-b538-000594f408e6',0,'${role_admin}','admin','faaacb96-1668-4dd7-b538-000594f408e6',NULL,NULL),('73437c5b-2dcc-4b96-adb2-9df7e255657c','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_query-groups}','query-groups','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('7a5d36bc-d21b-43a2-9887-7dd788f10103','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_query-clients}','query-clients','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('8165d16d-fedb-40bb-ad8c-bfaa90dc272b','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_manage-users}','manage-users','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('83933e1d-af79-4375-a2bf-d276db7c264f','c545dfde-c13c-40eb-bb45-72155bfcb98e',1,'${role_delete-account}','delete-account','faaacb96-1668-4dd7-b538-000594f408e6','c545dfde-c13c-40eb-bb45-72155bfcb98e',NULL),('888cbfc4-6b0a-4f5b-8414-ebb46446d0c3','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_manage-organizations}','manage-organizations','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('8b0cd07f-ad78-4aaf-bca9-dc7e7eb787ae','c545dfde-c13c-40eb-bb45-72155bfcb98e',1,'${role_manage-account}','manage-account','faaacb96-1668-4dd7-b538-000594f408e6','c545dfde-c13c-40eb-bb45-72155bfcb98e',NULL),('9e2f1ea3-984b-4f15-b7b9-92eb20587846','faaacb96-1668-4dd7-b538-000594f408e6',0,'${role_create-realm}','create-realm','faaacb96-1668-4dd7-b538-000594f408e6',NULL,NULL),('9f0ed45c-f548-4d3a-8735-8759c25ff57e','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_query-realms}','query-realms','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('b273ad17-cbac-4a38-b417-f349a6a39bfe','faaacb96-1668-4dd7-b538-000594f408e6',0,'${role_uma_authorization}','uma_authorization','faaacb96-1668-4dd7-b538-000594f408e6',NULL,NULL),('b73ae2aa-4dbc-49c7-9ede-ef898bcd2ae3','c545dfde-c13c-40eb-bb45-72155bfcb98e',1,'${role_view-groups}','view-groups','faaacb96-1668-4dd7-b538-000594f408e6','c545dfde-c13c-40eb-bb45-72155bfcb98e',NULL),('c17b1f42-9790-4707-993b-0ab08996ed40','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_manage-identity-providers}','manage-identity-providers','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('cd64029d-f471-44e3-882a-ae09917598db','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_manage-clients}','manage-clients','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('cd6a7c4c-99bf-444d-91fe-96ac7fc5be30','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_view-users}','view-users','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('d047fd38-c752-4bc8-8ed5-a36cde9021eb','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_manage-events}','manage-events','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('d2386173-4443-4607-b04c-a14ec55f8bdd','c545dfde-c13c-40eb-bb45-72155bfcb98e',1,'${role_manage-account-links}','manage-account-links','faaacb96-1668-4dd7-b538-000594f408e6','c545dfde-c13c-40eb-bb45-72155bfcb98e',NULL),('d24cd467-86fd-4c12-8d2b-242f6ff49ef9','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_impersonation}','impersonation','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('d463aee3-b627-4ca9-8d71-c2b46b1364af','faaacb96-1668-4dd7-b538-000594f408e6',0,'${role_default-roles}','default-roles-master','faaacb96-1668-4dd7-b538-000594f408e6',NULL,NULL),('d478be7f-f0b3-4a09-9fbd-3433ff355d22','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_manage-authorization}','manage-authorization','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('d4f67f7b-ce5c-494d-9a7d-4af24331c2b7','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_manage-realm}','manage-realm','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('e55b2fd6-f709-43cf-a676-ddb2dfc25fca','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_view-identity-providers}','view-identity-providers','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('eaeb0a6c-deda-439b-bd3c-4153206571c9','c545dfde-c13c-40eb-bb45-72155bfcb98e',1,'${role_manage-consent}','manage-consent','faaacb96-1668-4dd7-b538-000594f408e6','c545dfde-c13c-40eb-bb45-72155bfcb98e',NULL),('ee3990a6-0747-436e-a585-1e220d129b66','c545dfde-c13c-40eb-bb45-72155bfcb98e',1,'${role_view-consent}','view-consent','faaacb96-1668-4dd7-b538-000594f408e6','c545dfde-c13c-40eb-bb45-72155bfcb98e',NULL),('f7ff2d20-9d7b-4d43-a9bf-f1ac73c11021','c545dfde-c13c-40eb-bb45-72155bfcb98e',1,'${role_view-applications}','view-applications','faaacb96-1668-4dd7-b538-000594f408e6','c545dfde-c13c-40eb-bb45-72155bfcb98e',NULL),('fd9c0ffc-48a7-48ea-bd44-88f0908b2328','4573d9bb-a896-4da1-b70a-a364fdaee9a6',1,'${role_query-organizations}','query-organizations','faaacb96-1668-4dd7-b538-000594f408e6','4573d9bb-a896-4da1-b70a-a364fdaee9a6',NULL),('fe0685cc-69a7-4ea3-ac18-e725bd257988','c545dfde-c13c-40eb-bb45-72155bfcb98e',1,'${role_view-profile}','view-profile','faaacb96-1668-4dd7-b538-000594f408e6','c545dfde-c13c-40eb-bb45-72155bfcb98e',NULL);
UNLOCK TABLES;

--
-- Dumping data for table `login_failure`
--

LOCK TABLES `login_failure` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `migration_model`
--

LOCK TABLES `migration_model` WRITE;
INSERT INTO `migration_model` VALUES ('t3vqp','26.8.2',1794211594);
UNLOCK TABLES;

--
-- Dumping data for table `offline_client_session`
--

LOCK TABLES `offline_client_session` WRITE;
INSERT INTO `offline_client_session` VALUES ('7mHypGIioWszv-G9Tikn1lDr','05d101c8-6190-4dbc-9613-97d8d570f470','0',1794211603,'{\"authMethod\":\"openid-connect\",\"notes\":{\"clientId\":\"05d101c8-6190-4dbc-9613-97d8d570f470\",\"userSessionStartedAt\":\"1794211603\",\"iss\":\"http://keycloak:8080/auth/realms/master\",\"startedAt\":\"1794211603\",\"level-of-authentication\":\"-1\"}}','local','local',0,'faaacb96-1668-4dd7-b538-000594f408e6'),('8DqmYtOLr1oj2T_aoisj_Lh7','05d101c8-6190-4dbc-9613-97d8d570f470','0',1794211606,'{\"authMethod\":\"openid-connect\",\"notes\":{\"clientId\":\"05d101c8-6190-4dbc-9613-97d8d570f470\",\"userSessionStartedAt\":\"1794211606\",\"iss\":\"http://keycloak:8080/auth/realms/master\",\"startedAt\":\"1794211606\",\"level-of-authentication\":\"-1\"}}','local','local',0,'faaacb96-1668-4dd7-b538-000594f408e6'),('kDb4x9QsMk2nyo4G2W0U-1Xg','05d101c8-6190-4dbc-9613-97d8d570f470','0',1794211607,'{\"authMethod\":\"openid-connect\",\"notes\":{\"clientId\":\"05d101c8-6190-4dbc-9613-97d8d570f470\",\"userSessionStartedAt\":\"1794211607\",\"iss\":\"http://keycloak:8080/auth/realms/master\",\"startedAt\":\"1794211607\",\"level-of-authentication\":\"-1\"}}','local','local',0,'faaacb96-1668-4dd7-b538-000594f408e6'),('Qhj8OeRCQqj4JmzxkCq_3hYM','05d101c8-6190-4dbc-9613-97d8d570f470','0',1794211607,'{\"authMethod\":\"openid-connect\",\"notes\":{\"clientId\":\"05d101c8-6190-4dbc-9613-97d8d570f470\",\"userSessionStartedAt\":\"1794211607\",\"iss\":\"http://keycloak:8080/auth/realms/master\",\"startedAt\":\"1794211607\",\"level-of-authentication\":\"-1\"}}','local','local',0,'faaacb96-1668-4dd7-b538-000594f408e6'),('YPIvUPlg5Mr9ZjuCSyCd79im','05d101c8-6190-4dbc-9613-97d8d570f470','0',1794211602,'{\"authMethod\":\"openid-connect\",\"notes\":{\"clientId\":\"05d101c8-6190-4dbc-9613-97d8d570f470\",\"userSessionStartedAt\":\"1794211602\",\"iss\":\"http://keycloak:8080/auth/realms/master\",\"startedAt\":\"1794211602\",\"level-of-authentication\":\"-1\"}}','local','local',0,'faaacb96-1668-4dd7-b538-000594f408e6');
UNLOCK TABLES;

--
-- Dumping data for table `offline_user_session`
--

LOCK TABLES `offline_user_session` WRITE;
INSERT INTO `offline_user_session` VALUES ('7mHypGIioWszv-G9Tikn1lDr','3e7ffc4a-1e47-4508-b506-4e21d9458ce1','faaacb96-1668-4dd7-b538-000594f408e6',1794211603,'0','{\"ipAddress\":\"172.20.0.20\",\"authMethod\":\"openid-connect\",\"rememberMe\":false,\"started\":0,\"notes\":{\"KC_DEVICE_NOTE\":\"eyJpcEFkZHJlc3MiOiIxNzIuMjAuMC4yMCIsIm9zIjoiT3RoZXIiLCJvc1ZlcnNpb24iOiJVbmtub3duIiwiYnJvd3NlciI6IlB5dGhvbiBSZXF1ZXN0cy8yLjM0IiwiZGV2aWNlIjoiT3RoZXIiLCJsYXN0QWNjZXNzIjowLCJtb2JpbGUiOmZhbHNlfQ==\",\"authenticators-completed\":\"{\\\"65a27b14-e080-42bb-9761-e48494957a52\\\":1794211603,\\\"4c5ca8d7-02e6-46f2-91a3-e87c76ec6251\\\":1794211603}\"},\"state\":\"LOGGED_IN\"}',1794211603,NULL,0,0,23,1794211603),('8DqmYtOLr1oj2T_aoisj_Lh7','3e7ffc4a-1e47-4508-b506-4e21d9458ce1','faaacb96-1668-4dd7-b538-000594f408e6',1794211606,'0','{\"ipAddress\":\"172.20.0.20\",\"authMethod\":\"openid-connect\",\"rememberMe\":false,\"started\":0,\"notes\":{\"KC_DEVICE_NOTE\":\"eyJpcEFkZHJlc3MiOiIxNzIuMjAuMC4yMCIsIm9zIjoiT3RoZXIiLCJvc1ZlcnNpb24iOiJVbmtub3duIiwiYnJvd3NlciI6IlB5dGhvbiBSZXF1ZXN0cy8yLjM0IiwiZGV2aWNlIjoiT3RoZXIiLCJsYXN0QWNjZXNzIjowLCJtb2JpbGUiOmZhbHNlfQ==\",\"authenticators-completed\":\"{\\\"65a27b14-e080-42bb-9761-e48494957a52\\\":1794211606,\\\"4c5ca8d7-02e6-46f2-91a3-e87c76ec6251\\\":1794211606}\"},\"state\":\"LOGGED_IN\"}',1794211606,NULL,0,0,43,1794211606),('kDb4x9QsMk2nyo4G2W0U-1Xg','3e7ffc4a-1e47-4508-b506-4e21d9458ce1','faaacb96-1668-4dd7-b538-000594f408e6',1794211607,'0','{\"ipAddress\":\"172.20.0.20\",\"authMethod\":\"openid-connect\",\"rememberMe\":false,\"started\":0,\"notes\":{\"KC_DEVICE_NOTE\":\"eyJpcEFkZHJlc3MiOiIxNzIuMjAuMC4yMCIsIm9zIjoiT3RoZXIiLCJvc1ZlcnNpb24iOiJVbmtub3duIiwiYnJvd3NlciI6IlB5dGhvbiBSZXF1ZXN0cy8yLjM0IiwiZGV2aWNlIjoiT3RoZXIiLCJsYXN0QWNjZXNzIjowLCJtb2JpbGUiOmZhbHNlfQ==\",\"authenticators-completed\":\"{\\\"65a27b14-e080-42bb-9761-e48494957a52\\\":1794211607,\\\"4c5ca8d7-02e6-46f2-91a3-e87c76ec6251\\\":1794211607}\"},\"state\":\"LOGGED_IN\"}',1794211607,NULL,0,0,46,1794211607),('Qhj8OeRCQqj4JmzxkCq_3hYM','3e7ffc4a-1e47-4508-b506-4e21d9458ce1','faaacb96-1668-4dd7-b538-000594f408e6',1794211607,'0','{\"ipAddress\":\"172.20.0.20\",\"authMethod\":\"openid-connect\",\"rememberMe\":false,\"started\":0,\"notes\":{\"KC_DEVICE_NOTE\":\"eyJpcEFkZHJlc3MiOiIxNzIuMjAuMC4yMCIsIm9zIjoiT3RoZXIiLCJvc1ZlcnNpb24iOiJVbmtub3duIiwiYnJvd3NlciI6IlB5dGhvbiBSZXF1ZXN0cy8yLjM0IiwiZGV2aWNlIjoiT3RoZXIiLCJsYXN0QWNjZXNzIjowLCJtb2JpbGUiOmZhbHNlfQ==\",\"authenticators-completed\":\"{\\\"65a27b14-e080-42bb-9761-e48494957a52\\\":1794211607,\\\"4c5ca8d7-02e6-46f2-91a3-e87c76ec6251\\\":1794211607}\"},\"state\":\"LOGGED_IN\"}',1794211607,NULL,0,0,6,1794211607),('YPIvUPlg5Mr9ZjuCSyCd79im','3e7ffc4a-1e47-4508-b506-4e21d9458ce1','faaacb96-1668-4dd7-b538-000594f408e6',1794211602,'0','{\"ipAddress\":\"172.20.0.20\",\"authMethod\":\"openid-connect\",\"rememberMe\":false,\"started\":0,\"notes\":{\"KC_DEVICE_NOTE\":\"eyJpcEFkZHJlc3MiOiIxNzIuMjAuMC4yMCIsIm9zIjoiT3RoZXIiLCJvc1ZlcnNpb24iOiJVbmtub3duIiwiYnJvd3NlciI6IlB5dGhvbiBSZXF1ZXN0cy8yLjM0IiwiZGV2aWNlIjoiT3RoZXIiLCJsYXN0QWNjZXNzIjowLCJtb2JpbGUiOmZhbHNlfQ==\",\"authenticators-completed\":\"{\\\"65a27b14-e080-42bb-9761-e48494957a52\\\":1794211602,\\\"4c5ca8d7-02e6-46f2-91a3-e87c76ec6251\\\":1794211602}\"},\"state\":\"LOGGED_IN\"}',1794211602,NULL,0,0,4,1794211602);
UNLOCK TABLES;

--
-- Dumping data for table `org`
--

LOCK TABLES `org` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `org_domain`
--

LOCK TABLES `org_domain` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `org_identity_provider`
--

LOCK TABLES `org_identity_provider` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `org_invitation`
--

LOCK TABLES `org_invitation` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `outbox_entry`
--

LOCK TABLES `outbox_entry` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `policy_config`
--

LOCK TABLES `policy_config` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `protocol_mapper`
--

LOCK TABLES `protocol_mapper` WRITE;
INSERT INTO `protocol_mapper` VALUES ('0399f4a4-3ab8-4b2a-a9c5-18e81266b62f','phone number','openid-connect','oidc-usermodel-attribute-mapper',NULL,'4acbebfd-4e12-4551-afc9-6ea3682610a3'),('048bb2b3-d282-45aa-aedc-cb8f6101c4df','role list','saml','saml-role-list-mapper',NULL,'61f99739-6fce-43f9-958e-f3ea982b6e55'),('08aa1273-abc6-4caa-9ce7-f2d91a4608ac','Client ID','openid-connect','oidc-usersessionmodel-note-mapper',NULL,'2bbe7b9a-bdc7-4fff-94e6-bdc3584856da'),('152f7f09-b0f9-48f4-aa97-ea92a9a50244','picture','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('1c0c40d2-d3a1-4566-8d83-cb1e357715cd','profile','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('21378ae1-6e35-4ce5-b3d7-3993e4d3fe77','auth_time','openid-connect','oidc-usersessionmodel-note-mapper',NULL,'42d1ea7a-f39d-49c8-8777-7fd6b457e871'),('22deeb7c-5795-4212-915b-b8f2fd1f887c','AuthnContextClassRef','saml','saml-authn-context-class-ref-mapper',NULL,'0b5b5753-25ad-41c5-b2fb-024f036c101a'),('2a6255bc-8584-49a2-9bee-843551916747','phone number verified','openid-connect','oidc-usermodel-attribute-mapper',NULL,'4acbebfd-4e12-4551-afc9-6ea3682610a3'),('30860402-f1fd-4c72-9d06-96ec1f84e80b','full name','openid-connect','oidc-full-name-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('3e613cd2-9ac7-45f0-af26-f247372a3267','allowed web origins','openid-connect','oidc-allowed-origins-mapper',NULL,'67d5f582-ecc0-42d6-9f65-2c0452d5e397'),('4596cda2-47df-45dd-be9c-e190f8f81c64','groups','openid-connect','oidc-usermodel-realm-role-mapper',NULL,'5f5b905a-4d28-40f1-8350-99dfd37c904e'),('47184787-9974-4e5c-8c57-f8d4f3520168','upn','openid-connect','oidc-usermodel-attribute-mapper',NULL,'5f5b905a-4d28-40f1-8350-99dfd37c904e'),('48b0c01a-5b69-4756-85c6-c84812537f83','zoneinfo','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('4d051a19-2db6-43f5-80a8-6bd542f0b079','given name','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('4ee05591-0a1e-49c8-8a0f-b950dadafe42','audience resolve','openid-connect','oidc-audience-resolve-mapper',NULL,'349cd61f-65a1-4f1e-9370-de157d8a9920'),('50a65d02-1d55-45d9-86fb-da65f377ee7e','Client IP Address','openid-connect','oidc-usersessionmodel-note-mapper','0060978e-25c0-4f54-9b7b-74dbd36df936',NULL),('6946e320-9078-42ef-b904-19ac27400f48','middle name','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('699a0cf7-5601-4a46-98d5-32dd58fd2d40','updated at','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('6bf55daf-14fa-41e0-b3db-ecc7cbfb436f','audience-_platform','openid-connect','oidc-audience-mapper','0060978e-25c0-4f54-9b7b-74dbd36df936',NULL),('762dcd20-b0dd-4717-a9b1-ddde28f29685','email verified','openid-connect','oidc-usermodel-property-mapper',NULL,'1fdb82c7-6ab9-4d1f-b608-bd2f525fe810'),('83208a5d-c242-4cc0-995f-df6837c69df9','email','openid-connect','oidc-usermodel-attribute-mapper',NULL,'1fdb82c7-6ab9-4d1f-b608-bd2f525fe810'),('84cc47e7-ab73-488e-8549-dbe59bdeb162','audience-_platform','openid-connect','oidc-audience-mapper','54c52862-bb56-483f-85dd-e529c984b618',NULL),('8db340a2-b73c-4de9-ba12-886856cf3ab3','Client Host','openid-connect','oidc-usersessionmodel-note-mapper','0060978e-25c0-4f54-9b7b-74dbd36df936',NULL),('93bc66af-7ca4-44b5-b81b-8e858bd6de5e','locale','openid-connect','oidc-usermodel-attribute-mapper','7085a323-1455-4f1b-97f7-bfe1ffa52de8',NULL),('951497ce-f74a-4ecb-8245-1f384489642b','audience-_platform','openid-connect','oidc-audience-mapper','7d911892-0def-4068-9047-457bdb014ab8',NULL),('951b683a-baf2-49cf-af50-170334e5b51f','gender','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('97bf3312-7016-40ac-aeff-501d1d4bff95','website','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('9966f331-e916-41cc-ae75-ec55231f06e0','username','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('9a7097f7-51e2-4fb1-8652-987db151971b','realm roles','openid-connect','oidc-usermodel-realm-role-mapper',NULL,'349cd61f-65a1-4f1e-9370-de157d8a9920'),('a37c7e4a-c66a-4188-987c-2c4c8750c1bc','birthdate','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','address','openid-connect','oidc-address-mapper',NULL,'9be0037a-51a5-4eb3-b14a-24d9135ffd1c'),('a986af8d-9ea9-4cb1-ba16-1429d0902557','organization','saml','saml-organization-membership-mapper',NULL,'5ac886e2-fbb9-44b5-9ff9-dbe4fa973d3f'),('c6465c9c-21e1-4c00-bf76-436bddf43cad','family name','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('c7011acd-b741-48ca-80f1-9184c4fd86a2','sub','openid-connect','oidc-sub-mapper',NULL,'42d1ea7a-f39d-49c8-8777-7fd6b457e871'),('c8278b42-f672-437b-9085-a93ec76236c5','audience resolve','openid-connect','oidc-audience-resolve-mapper','8c6458b8-7b08-46db-bcfd-f98c4a29714b',NULL),('c913639d-f713-42b3-88f1-b7eb318cda6f','admin-api-audience','openid-connect','oidc-admin-api-audience-mapper',NULL,'3ca64165-0619-47c2-9793-470f444c40c2'),('d1e7fb2d-14fd-42cc-8979-dd3c5197a0b9','locale','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('d4347e7c-0a67-4aa7-83d7-4a394e0b70d7','acr loa level','openid-connect','oidc-acr-mapper',NULL,'d14d6d0a-565b-48d1-b7d1-de0a879d723a'),('d52ed19a-ad66-4d0c-89b0-d54961477359','Client Host','openid-connect','oidc-usersessionmodel-note-mapper',NULL,'2bbe7b9a-bdc7-4fff-94e6-bdc3584856da'),('dfffd0b4-2f84-4b46-88ef-c2329b5ab6b5','Client IP Address','openid-connect','oidc-usersessionmodel-note-mapper',NULL,'2bbe7b9a-bdc7-4fff-94e6-bdc3584856da'),('e00d0477-f641-406e-bd4b-ec9cfea6dca3','nickname','openid-connect','oidc-usermodel-attribute-mapper',NULL,'23dd2041-cb93-488c-9ef0-910909a90987'),('eb6ff783-a11c-4a94-a93c-98f985c39a3f','client roles','openid-connect','oidc-usermodel-client-role-mapper',NULL,'349cd61f-65a1-4f1e-9370-de157d8a9920'),('ecb6c826-f2ac-4eb2-8fbd-b3e6895fd456','organization','openid-connect','oidc-organization-membership-mapper',NULL,'9e94b502-44b3-473d-a357-97ac8014913a'),('f3a550ec-9a2e-410d-b1ff-a501daad93e9','Client ID','openid-connect','oidc-usersessionmodel-note-mapper','0060978e-25c0-4f54-9b7b-74dbd36df936',NULL);
UNLOCK TABLES;

--
-- Dumping data for table `protocol_mapper_config`
--

LOCK TABLES `protocol_mapper_config` WRITE;
INSERT INTO `protocol_mapper_config` VALUES ('0399f4a4-3ab8-4b2a-a9c5-18e81266b62f','true','access.token.claim'),('0399f4a4-3ab8-4b2a-a9c5-18e81266b62f','phone_number','claim.name'),('0399f4a4-3ab8-4b2a-a9c5-18e81266b62f','true','id.token.claim'),('0399f4a4-3ab8-4b2a-a9c5-18e81266b62f','true','introspection.token.claim'),('0399f4a4-3ab8-4b2a-a9c5-18e81266b62f','String','jsonType.label'),('0399f4a4-3ab8-4b2a-a9c5-18e81266b62f','phoneNumber','user.attribute'),('0399f4a4-3ab8-4b2a-a9c5-18e81266b62f','true','userinfo.token.claim'),('048bb2b3-d282-45aa-aedc-cb8f6101c4df','Role','attribute.name'),('048bb2b3-d282-45aa-aedc-cb8f6101c4df','Basic','attribute.nameformat'),('048bb2b3-d282-45aa-aedc-cb8f6101c4df','false','single'),('08aa1273-abc6-4caa-9ce7-f2d91a4608ac','true','access.token.claim'),('08aa1273-abc6-4caa-9ce7-f2d91a4608ac','client_id','claim.name'),('08aa1273-abc6-4caa-9ce7-f2d91a4608ac','true','id.token.claim'),('08aa1273-abc6-4caa-9ce7-f2d91a4608ac','true','introspection.token.claim'),('08aa1273-abc6-4caa-9ce7-f2d91a4608ac','String','jsonType.label'),('08aa1273-abc6-4caa-9ce7-f2d91a4608ac','client_id','user.session.note'),('152f7f09-b0f9-48f4-aa97-ea92a9a50244','true','access.token.claim'),('152f7f09-b0f9-48f4-aa97-ea92a9a50244','picture','claim.name'),('152f7f09-b0f9-48f4-aa97-ea92a9a50244','true','id.token.claim'),('152f7f09-b0f9-48f4-aa97-ea92a9a50244','true','introspection.token.claim'),('152f7f09-b0f9-48f4-aa97-ea92a9a50244','String','jsonType.label'),('152f7f09-b0f9-48f4-aa97-ea92a9a50244','picture','user.attribute'),('152f7f09-b0f9-48f4-aa97-ea92a9a50244','true','userinfo.token.claim'),('1c0c40d2-d3a1-4566-8d83-cb1e357715cd','true','access.token.claim'),('1c0c40d2-d3a1-4566-8d83-cb1e357715cd','profile','claim.name'),('1c0c40d2-d3a1-4566-8d83-cb1e357715cd','true','id.token.claim'),('1c0c40d2-d3a1-4566-8d83-cb1e357715cd','true','introspection.token.claim'),('1c0c40d2-d3a1-4566-8d83-cb1e357715cd','String','jsonType.label'),('1c0c40d2-d3a1-4566-8d83-cb1e357715cd','profile','user.attribute'),('1c0c40d2-d3a1-4566-8d83-cb1e357715cd','true','userinfo.token.claim'),('21378ae1-6e35-4ce5-b3d7-3993e4d3fe77','true','access.token.claim'),('21378ae1-6e35-4ce5-b3d7-3993e4d3fe77','auth_time','claim.name'),('21378ae1-6e35-4ce5-b3d7-3993e4d3fe77','true','id.token.claim'),('21378ae1-6e35-4ce5-b3d7-3993e4d3fe77','true','introspection.token.claim'),('21378ae1-6e35-4ce5-b3d7-3993e4d3fe77','long','jsonType.label'),('21378ae1-6e35-4ce5-b3d7-3993e4d3fe77','AUTH_TIME','user.session.note'),('2a6255bc-8584-49a2-9bee-843551916747','true','access.token.claim'),('2a6255bc-8584-49a2-9bee-843551916747','phone_number_verified','claim.name'),('2a6255bc-8584-49a2-9bee-843551916747','true','id.token.claim'),('2a6255bc-8584-49a2-9bee-843551916747','true','introspection.token.claim'),('2a6255bc-8584-49a2-9bee-843551916747','boolean','jsonType.label'),('2a6255bc-8584-49a2-9bee-843551916747','phoneNumberVerified','user.attribute'),('2a6255bc-8584-49a2-9bee-843551916747','true','userinfo.token.claim'),('30860402-f1fd-4c72-9d06-96ec1f84e80b','true','access.token.claim'),('30860402-f1fd-4c72-9d06-96ec1f84e80b','true','id.token.claim'),('30860402-f1fd-4c72-9d06-96ec1f84e80b','true','introspection.token.claim'),('30860402-f1fd-4c72-9d06-96ec1f84e80b','true','userinfo.token.claim'),('3e613cd2-9ac7-45f0-af26-f247372a3267','true','access.token.claim'),('3e613cd2-9ac7-45f0-af26-f247372a3267','true','introspection.token.claim'),('4596cda2-47df-45dd-be9c-e190f8f81c64','true','access.token.claim'),('4596cda2-47df-45dd-be9c-e190f8f81c64','groups','claim.name'),('4596cda2-47df-45dd-be9c-e190f8f81c64','true','id.token.claim'),('4596cda2-47df-45dd-be9c-e190f8f81c64','true','introspection.token.claim'),('4596cda2-47df-45dd-be9c-e190f8f81c64','String','jsonType.label'),('4596cda2-47df-45dd-be9c-e190f8f81c64','true','multivalued'),('4596cda2-47df-45dd-be9c-e190f8f81c64','foo','user.attribute'),('47184787-9974-4e5c-8c57-f8d4f3520168','true','access.token.claim'),('47184787-9974-4e5c-8c57-f8d4f3520168','upn','claim.name'),('47184787-9974-4e5c-8c57-f8d4f3520168','true','id.token.claim'),('47184787-9974-4e5c-8c57-f8d4f3520168','true','introspection.token.claim'),('47184787-9974-4e5c-8c57-f8d4f3520168','String','jsonType.label'),('47184787-9974-4e5c-8c57-f8d4f3520168','username','user.attribute'),('47184787-9974-4e5c-8c57-f8d4f3520168','true','userinfo.token.claim'),('48b0c01a-5b69-4756-85c6-c84812537f83','true','access.token.claim'),('48b0c01a-5b69-4756-85c6-c84812537f83','zoneinfo','claim.name'),('48b0c01a-5b69-4756-85c6-c84812537f83','true','id.token.claim'),('48b0c01a-5b69-4756-85c6-c84812537f83','true','introspection.token.claim'),('48b0c01a-5b69-4756-85c6-c84812537f83','String','jsonType.label'),('48b0c01a-5b69-4756-85c6-c84812537f83','zoneinfo','user.attribute'),('48b0c01a-5b69-4756-85c6-c84812537f83','true','userinfo.token.claim'),('4d051a19-2db6-43f5-80a8-6bd542f0b079','true','access.token.claim'),('4d051a19-2db6-43f5-80a8-6bd542f0b079','given_name','claim.name'),('4d051a19-2db6-43f5-80a8-6bd542f0b079','true','id.token.claim'),('4d051a19-2db6-43f5-80a8-6bd542f0b079','true','introspection.token.claim'),('4d051a19-2db6-43f5-80a8-6bd542f0b079','String','jsonType.label'),('4d051a19-2db6-43f5-80a8-6bd542f0b079','firstName','user.attribute'),('4d051a19-2db6-43f5-80a8-6bd542f0b079','true','userinfo.token.claim'),('4ee05591-0a1e-49c8-8a0f-b950dadafe42','true','access.token.claim'),('4ee05591-0a1e-49c8-8a0f-b950dadafe42','true','introspection.token.claim'),('50a65d02-1d55-45d9-86fb-da65f377ee7e','true','access.token.claim'),('50a65d02-1d55-45d9-86fb-da65f377ee7e','clientAddress','claim.name'),('50a65d02-1d55-45d9-86fb-da65f377ee7e','true','id.token.claim'),('50a65d02-1d55-45d9-86fb-da65f377ee7e','String','jsonType.label'),('50a65d02-1d55-45d9-86fb-da65f377ee7e','clientAddress','user.session.note'),('50a65d02-1d55-45d9-86fb-da65f377ee7e','true','userinfo.token.claim'),('6946e320-9078-42ef-b904-19ac27400f48','true','access.token.claim'),('6946e320-9078-42ef-b904-19ac27400f48','middle_name','claim.name'),('6946e320-9078-42ef-b904-19ac27400f48','true','id.token.claim'),('6946e320-9078-42ef-b904-19ac27400f48','true','introspection.token.claim'),('6946e320-9078-42ef-b904-19ac27400f48','String','jsonType.label'),('6946e320-9078-42ef-b904-19ac27400f48','middleName','user.attribute'),('6946e320-9078-42ef-b904-19ac27400f48','true','userinfo.token.claim'),('699a0cf7-5601-4a46-98d5-32dd58fd2d40','true','access.token.claim'),('699a0cf7-5601-4a46-98d5-32dd58fd2d40','updated_at','claim.name'),('699a0cf7-5601-4a46-98d5-32dd58fd2d40','true','id.token.claim'),('699a0cf7-5601-4a46-98d5-32dd58fd2d40','true','introspection.token.claim'),('699a0cf7-5601-4a46-98d5-32dd58fd2d40','long','jsonType.label'),('699a0cf7-5601-4a46-98d5-32dd58fd2d40','updatedAt','user.attribute'),('699a0cf7-5601-4a46-98d5-32dd58fd2d40','true','userinfo.token.claim'),('6bf55daf-14fa-41e0-b3db-ecc7cbfb436f','true','access.token.claim'),('6bf55daf-14fa-41e0-b3db-ecc7cbfb436f','false','id.token.claim'),('6bf55daf-14fa-41e0-b3db-ecc7cbfb436f','_platform','included.client.audience'),('6bf55daf-14fa-41e0-b3db-ecc7cbfb436f','true','introspection.token.claim'),('6bf55daf-14fa-41e0-b3db-ecc7cbfb436f','false','userinfo.token.claim'),('762dcd20-b0dd-4717-a9b1-ddde28f29685','true','access.token.claim'),('762dcd20-b0dd-4717-a9b1-ddde28f29685','email_verified','claim.name'),('762dcd20-b0dd-4717-a9b1-ddde28f29685','true','id.token.claim'),('762dcd20-b0dd-4717-a9b1-ddde28f29685','true','introspection.token.claim'),('762dcd20-b0dd-4717-a9b1-ddde28f29685','boolean','jsonType.label'),('762dcd20-b0dd-4717-a9b1-ddde28f29685','emailVerified','user.attribute'),('762dcd20-b0dd-4717-a9b1-ddde28f29685','true','userinfo.token.claim'),('83208a5d-c242-4cc0-995f-df6837c69df9','true','access.token.claim'),('83208a5d-c242-4cc0-995f-df6837c69df9','email','claim.name'),('83208a5d-c242-4cc0-995f-df6837c69df9','true','id.token.claim'),('83208a5d-c242-4cc0-995f-df6837c69df9','true','introspection.token.claim'),('83208a5d-c242-4cc0-995f-df6837c69df9','String','jsonType.label'),('83208a5d-c242-4cc0-995f-df6837c69df9','email','user.attribute'),('83208a5d-c242-4cc0-995f-df6837c69df9','true','userinfo.token.claim'),('84cc47e7-ab73-488e-8549-dbe59bdeb162','true','access.token.claim'),('84cc47e7-ab73-488e-8549-dbe59bdeb162','false','id.token.claim'),('84cc47e7-ab73-488e-8549-dbe59bdeb162','_platform','included.client.audience'),('84cc47e7-ab73-488e-8549-dbe59bdeb162','true','introspection.token.claim'),('84cc47e7-ab73-488e-8549-dbe59bdeb162','false','userinfo.token.claim'),('8db340a2-b73c-4de9-ba12-886856cf3ab3','true','access.token.claim'),('8db340a2-b73c-4de9-ba12-886856cf3ab3','clientHost','claim.name'),('8db340a2-b73c-4de9-ba12-886856cf3ab3','true','id.token.claim'),('8db340a2-b73c-4de9-ba12-886856cf3ab3','String','jsonType.label'),('8db340a2-b73c-4de9-ba12-886856cf3ab3','clientHost','user.session.note'),('8db340a2-b73c-4de9-ba12-886856cf3ab3','true','userinfo.token.claim'),('93bc66af-7ca4-44b5-b81b-8e858bd6de5e','true','access.token.claim'),('93bc66af-7ca4-44b5-b81b-8e858bd6de5e','locale','claim.name'),('93bc66af-7ca4-44b5-b81b-8e858bd6de5e','true','id.token.claim'),('93bc66af-7ca4-44b5-b81b-8e858bd6de5e','true','introspection.token.claim'),('93bc66af-7ca4-44b5-b81b-8e858bd6de5e','String','jsonType.label'),('93bc66af-7ca4-44b5-b81b-8e858bd6de5e','locale','user.attribute'),('93bc66af-7ca4-44b5-b81b-8e858bd6de5e','true','userinfo.token.claim'),('951497ce-f74a-4ecb-8245-1f384489642b','true','access.token.claim'),('951497ce-f74a-4ecb-8245-1f384489642b','false','id.token.claim'),('951497ce-f74a-4ecb-8245-1f384489642b','_platform','included.client.audience'),('951b683a-baf2-49cf-af50-170334e5b51f','true','access.token.claim'),('951b683a-baf2-49cf-af50-170334e5b51f','gender','claim.name'),('951b683a-baf2-49cf-af50-170334e5b51f','true','id.token.claim'),('951b683a-baf2-49cf-af50-170334e5b51f','true','introspection.token.claim'),('951b683a-baf2-49cf-af50-170334e5b51f','String','jsonType.label'),('951b683a-baf2-49cf-af50-170334e5b51f','gender','user.attribute'),('951b683a-baf2-49cf-af50-170334e5b51f','true','userinfo.token.claim'),('97bf3312-7016-40ac-aeff-501d1d4bff95','true','access.token.claim'),('97bf3312-7016-40ac-aeff-501d1d4bff95','website','claim.name'),('97bf3312-7016-40ac-aeff-501d1d4bff95','true','id.token.claim'),('97bf3312-7016-40ac-aeff-501d1d4bff95','true','introspection.token.claim'),('97bf3312-7016-40ac-aeff-501d1d4bff95','String','jsonType.label'),('97bf3312-7016-40ac-aeff-501d1d4bff95','website','user.attribute'),('97bf3312-7016-40ac-aeff-501d1d4bff95','true','userinfo.token.claim'),('9966f331-e916-41cc-ae75-ec55231f06e0','true','access.token.claim'),('9966f331-e916-41cc-ae75-ec55231f06e0','preferred_username','claim.name'),('9966f331-e916-41cc-ae75-ec55231f06e0','true','id.token.claim'),('9966f331-e916-41cc-ae75-ec55231f06e0','true','introspection.token.claim'),('9966f331-e916-41cc-ae75-ec55231f06e0','String','jsonType.label'),('9966f331-e916-41cc-ae75-ec55231f06e0','username','user.attribute'),('9966f331-e916-41cc-ae75-ec55231f06e0','true','userinfo.token.claim'),('9a7097f7-51e2-4fb1-8652-987db151971b','true','access.token.claim'),('9a7097f7-51e2-4fb1-8652-987db151971b','realm_access.roles','claim.name'),('9a7097f7-51e2-4fb1-8652-987db151971b','true','introspection.token.claim'),('9a7097f7-51e2-4fb1-8652-987db151971b','String','jsonType.label'),('9a7097f7-51e2-4fb1-8652-987db151971b','true','multivalued'),('9a7097f7-51e2-4fb1-8652-987db151971b','foo','user.attribute'),('a37c7e4a-c66a-4188-987c-2c4c8750c1bc','true','access.token.claim'),('a37c7e4a-c66a-4188-987c-2c4c8750c1bc','birthdate','claim.name'),('a37c7e4a-c66a-4188-987c-2c4c8750c1bc','true','id.token.claim'),('a37c7e4a-c66a-4188-987c-2c4c8750c1bc','true','introspection.token.claim'),('a37c7e4a-c66a-4188-987c-2c4c8750c1bc','String','jsonType.label'),('a37c7e4a-c66a-4188-987c-2c4c8750c1bc','birthdate','user.attribute'),('a37c7e4a-c66a-4188-987c-2c4c8750c1bc','true','userinfo.token.claim'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','true','access.token.claim'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','true','id.token.claim'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','true','introspection.token.claim'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','country','user.attribute.country'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','formatted','user.attribute.formatted'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','locality','user.attribute.locality'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','postal_code','user.attribute.postal_code'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','region','user.attribute.region'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','street','user.attribute.street'),('a8bb7db5-dc01-4b8c-8aae-63646cfac564','true','userinfo.token.claim'),('c6465c9c-21e1-4c00-bf76-436bddf43cad','true','access.token.claim'),('c6465c9c-21e1-4c00-bf76-436bddf43cad','family_name','claim.name'),('c6465c9c-21e1-4c00-bf76-436bddf43cad','true','id.token.claim'),('c6465c9c-21e1-4c00-bf76-436bddf43cad','true','introspection.token.claim'),('c6465c9c-21e1-4c00-bf76-436bddf43cad','String','jsonType.label'),('c6465c9c-21e1-4c00-bf76-436bddf43cad','lastName','user.attribute'),('c6465c9c-21e1-4c00-bf76-436bddf43cad','true','userinfo.token.claim'),('c7011acd-b741-48ca-80f1-9184c4fd86a2','true','access.token.claim'),('c7011acd-b741-48ca-80f1-9184c4fd86a2','true','introspection.token.claim'),('c913639d-f713-42b3-88f1-b7eb318cda6f','true','access.token.claim'),('c913639d-f713-42b3-88f1-b7eb318cda6f','true','introspection.token.claim'),('c913639d-f713-42b3-88f1-b7eb318cda6f','true','lightweight.claim'),('d1e7fb2d-14fd-42cc-8979-dd3c5197a0b9','true','access.token.claim'),('d1e7fb2d-14fd-42cc-8979-dd3c5197a0b9','locale','claim.name'),('d1e7fb2d-14fd-42cc-8979-dd3c5197a0b9','true','id.token.claim'),('d1e7fb2d-14fd-42cc-8979-dd3c5197a0b9','true','introspection.token.claim'),('d1e7fb2d-14fd-42cc-8979-dd3c5197a0b9','String','jsonType.label'),('d1e7fb2d-14fd-42cc-8979-dd3c5197a0b9','locale','user.attribute'),('d1e7fb2d-14fd-42cc-8979-dd3c5197a0b9','true','userinfo.token.claim'),('d4347e7c-0a67-4aa7-83d7-4a394e0b70d7','true','access.token.claim'),('d4347e7c-0a67-4aa7-83d7-4a394e0b70d7','true','id.token.claim'),('d4347e7c-0a67-4aa7-83d7-4a394e0b70d7','true','introspection.token.claim'),('d52ed19a-ad66-4d0c-89b0-d54961477359','true','access.token.claim'),('d52ed19a-ad66-4d0c-89b0-d54961477359','clientHost','claim.name'),('d52ed19a-ad66-4d0c-89b0-d54961477359','true','id.token.claim'),('d52ed19a-ad66-4d0c-89b0-d54961477359','true','introspection.token.claim'),('d52ed19a-ad66-4d0c-89b0-d54961477359','String','jsonType.label'),('d52ed19a-ad66-4d0c-89b0-d54961477359','clientHost','user.session.note'),('dfffd0b4-2f84-4b46-88ef-c2329b5ab6b5','true','access.token.claim'),('dfffd0b4-2f84-4b46-88ef-c2329b5ab6b5','clientAddress','claim.name'),('dfffd0b4-2f84-4b46-88ef-c2329b5ab6b5','true','id.token.claim'),('dfffd0b4-2f84-4b46-88ef-c2329b5ab6b5','true','introspection.token.claim'),('dfffd0b4-2f84-4b46-88ef-c2329b5ab6b5','String','jsonType.label'),('dfffd0b4-2f84-4b46-88ef-c2329b5ab6b5','clientAddress','user.session.note'),('e00d0477-f641-406e-bd4b-ec9cfea6dca3','true','access.token.claim'),('e00d0477-f641-406e-bd4b-ec9cfea6dca3','nickname','claim.name'),('e00d0477-f641-406e-bd4b-ec9cfea6dca3','true','id.token.claim'),('e00d0477-f641-406e-bd4b-ec9cfea6dca3','true','introspection.token.claim'),('e00d0477-f641-406e-bd4b-ec9cfea6dca3','String','jsonType.label'),('e00d0477-f641-406e-bd4b-ec9cfea6dca3','nickname','user.attribute'),('e00d0477-f641-406e-bd4b-ec9cfea6dca3','true','userinfo.token.claim'),('eb6ff783-a11c-4a94-a93c-98f985c39a3f','true','access.token.claim'),('eb6ff783-a11c-4a94-a93c-98f985c39a3f','resource_access.${client_id}.roles','claim.name'),('eb6ff783-a11c-4a94-a93c-98f985c39a3f','true','introspection.token.claim'),('eb6ff783-a11c-4a94-a93c-98f985c39a3f','String','jsonType.label'),('eb6ff783-a11c-4a94-a93c-98f985c39a3f','true','multivalued'),('eb6ff783-a11c-4a94-a93c-98f985c39a3f','foo','user.attribute'),('ecb6c826-f2ac-4eb2-8fbd-b3e6895fd456','true','access.token.claim'),('ecb6c826-f2ac-4eb2-8fbd-b3e6895fd456','organization','claim.name'),('ecb6c826-f2ac-4eb2-8fbd-b3e6895fd456','true','id.token.claim'),('ecb6c826-f2ac-4eb2-8fbd-b3e6895fd456','true','introspection.token.claim'),('ecb6c826-f2ac-4eb2-8fbd-b3e6895fd456','String','jsonType.label'),('ecb6c826-f2ac-4eb2-8fbd-b3e6895fd456','true','multivalued'),('f3a550ec-9a2e-410d-b1ff-a501daad93e9','true','access.token.claim'),('f3a550ec-9a2e-410d-b1ff-a501daad93e9','clientId','claim.name'),('f3a550ec-9a2e-410d-b1ff-a501daad93e9','true','id.token.claim'),('f3a550ec-9a2e-410d-b1ff-a501daad93e9','String','jsonType.label'),('f3a550ec-9a2e-410d-b1ff-a501daad93e9','clientId','user.session.note'),('f3a550ec-9a2e-410d-b1ff-a501daad93e9','true','userinfo.token.claim');
UNLOCK TABLES;

--
-- Dumping data for table `realm`
--

LOCK TABLES `realm` WRITE;
INSERT INTO `realm` VALUES ('faaacb96-1668-4dd7-b538-000594f408e6',60,300,60,NULL,NULL,NULL,1,0,0,'exastro','master',0,NULL,0,0,0,0,'NONE',86400,86400,0,0,'4573d9bb-a896-4da1-b70a-a364fdaee9a6',1800,1,'ja',0,0,0,0,0,1,30,6,'HmacSHA1','totp','1f73705a-3eed-4433-9b87-68f9aa788717','7b08e83a-e376-42ff-8b86-e8cf756691a0','f90efcf4-2095-41b5-abd1-93c4420436d4','00614996-4f54-4c94-855d-18ba4c98ffc3','cacb068a-38fa-454b-9b33-251c9a54669c',31536000,0,900,1,0,'726ff5d4-3bde-4d80-b4d6-43b597c55e68',0,0,0,0,'d463aee3-b627-4ca9-8d71-c2b46b1364af','Keycloak');
UNLOCK TABLES;

--
-- Dumping data for table `realm_attribute`
--

LOCK TABLES `realm_attribute` WRITE;
INSERT INTO `realm_attribute` VALUES ('_browser_header.contentSecurityPolicy','faaacb96-1668-4dd7-b538-000594f408e6','frame-src \'self\'; frame-ancestors \'self\'; object-src \'none\';'),('_browser_header.contentSecurityPolicyReportOnly','faaacb96-1668-4dd7-b538-000594f408e6',''),('_browser_header.referrerPolicy','faaacb96-1668-4dd7-b538-000594f408e6','no-referrer'),('_browser_header.strictTransportSecurity','faaacb96-1668-4dd7-b538-000594f408e6','max-age=31536000; includeSubDomains'),('_browser_header.xContentTypeOptions','faaacb96-1668-4dd7-b538-000594f408e6','nosniff'),('_browser_header.xFrameOptions','faaacb96-1668-4dd7-b538-000594f408e6','SAMEORIGIN'),('_browser_header.xRobotsTag','faaacb96-1668-4dd7-b538-000594f408e6','none'),('bruteForceProtected','faaacb96-1668-4dd7-b538-000594f408e6','false'),('bruteForceStrategy','faaacb96-1668-4dd7-b538-000594f408e6','MULTIPLE'),('cibaAuthRequestedUserHint','faaacb96-1668-4dd7-b538-000594f408e6','login_hint'),('cibaBackchannelTokenDeliveryMode','faaacb96-1668-4dd7-b538-000594f408e6','poll'),('cibaExpiresIn','faaacb96-1668-4dd7-b538-000594f408e6','120'),('cibaInterval','faaacb96-1668-4dd7-b538-000594f408e6','5'),('defaultSignatureAlgorithm','faaacb96-1668-4dd7-b538-000594f408e6','RS256'),('displayNameHtml','faaacb96-1668-4dd7-b538-000594f408e6','<div class=\"kc-logo-text\"><span>Keycloak</span></div>'),('failureFactor','faaacb96-1668-4dd7-b538-000594f408e6','30'),('firstBrokerLoginFlowId','faaacb96-1668-4dd7-b538-000594f408e6','2b32921f-c16d-4224-8e9b-c1b9ed64b58d'),('maxDeltaTimeSeconds','faaacb96-1668-4dd7-b538-000594f408e6','43200'),('maxFailureWaitSeconds','faaacb96-1668-4dd7-b538-000594f408e6','900'),('maxSecondaryAuthFailures','faaacb96-1668-4dd7-b538-000594f408e6','0'),('maxTemporaryLockouts','faaacb96-1668-4dd7-b538-000594f408e6','0'),('minimumQuickLoginWaitSeconds','faaacb96-1668-4dd7-b538-000594f408e6','60'),('oauth2DeviceCodeLifespan','faaacb96-1668-4dd7-b538-000594f408e6','600'),('oauth2DevicePollingInterval','faaacb96-1668-4dd7-b538-000594f408e6','5'),('offlineSessionMaxLifespan','faaacb96-1668-4dd7-b538-000594f408e6','31536000'),('offlineSessionMaxLifespanEnabled','faaacb96-1668-4dd7-b538-000594f408e6','true'),('parRequestUriLifespan','faaacb96-1668-4dd7-b538-000594f408e6','60'),('permanentLockout','faaacb96-1668-4dd7-b538-000594f408e6','false'),('quickLoginCheckMilliSeconds','faaacb96-1668-4dd7-b538-000594f408e6','1000'),('realmReusableOtpCode','faaacb96-1668-4dd7-b538-000594f408e6','false'),('waitIncrementSeconds','faaacb96-1668-4dd7-b538-000594f408e6','60');
UNLOCK TABLES;

--
-- Dumping data for table `realm_default_groups`
--

LOCK TABLES `realm_default_groups` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `realm_enabled_event_types`
--

LOCK TABLES `realm_enabled_event_types` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `realm_events_listeners`
--

LOCK TABLES `realm_events_listeners` WRITE;
INSERT INTO `realm_events_listeners` VALUES ('faaacb96-1668-4dd7-b538-000594f408e6','jboss-logging');
UNLOCK TABLES;

--
-- Dumping data for table `realm_localizations`
--

LOCK TABLES `realm_localizations` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `realm_required_credential`
--

LOCK TABLES `realm_required_credential` WRITE;
INSERT INTO `realm_required_credential` VALUES ('password','password',1,1,'faaacb96-1668-4dd7-b538-000594f408e6');
UNLOCK TABLES;

--
-- Dumping data for table `realm_smtp_config`
--

LOCK TABLES `realm_smtp_config` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `realm_supported_locales`
--

LOCK TABLES `realm_supported_locales` WRITE;
INSERT INTO `realm_supported_locales` VALUES ('faaacb96-1668-4dd7-b538-000594f408e6','en'),('faaacb96-1668-4dd7-b538-000594f408e6','ja');
UNLOCK TABLES;

--
-- Dumping data for table `redirect_uris`
--

LOCK TABLES `redirect_uris` WRITE;
INSERT INTO `redirect_uris` VALUES ('7085a323-1455-4f1b-97f7-bfe1ffa52de8','/admin/master/console/*'),('7d911892-0def-4068-9047-457bdb014ab8','/*'),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','/realms/master/account/*'),('c545dfde-c13c-40eb-bb45-72155bfcb98e','/realms/master/account/*');
UNLOCK TABLES;

--
-- Dumping data for table `required_action_config`
--

LOCK TABLES `required_action_config` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `required_action_provider`
--

LOCK TABLES `required_action_provider` WRITE;
INSERT INTO `required_action_provider` VALUES ('197cce5c-3914-49ae-9b87-55e915d42cdc','VERIFY_EMAIL','Verify Email','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'VERIFY_EMAIL',50),('277522b7-52c6-4560-b8aa-4741bc14a070','UPDATE_PROFILE','Update Profile','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'UPDATE_PROFILE',40),('2ed5c2b9-ea00-4594-a8c1-07f155efd34f','delete_account','Delete Account','faaacb96-1668-4dd7-b538-000594f408e6',0,0,'delete_account',60),('304855b9-b5e0-40d0-a128-09e31aea690a','update_user_locale','Update User Locale','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'update_user_locale',1000),('3b75802e-dc63-44d1-a084-7069a6d62d86','CONFIGURE_TOTP','Configure OTP','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'CONFIGURE_TOTP',54),('44fadbb9-a59d-4706-a6b4-a50739df5e4f','webauthn-register-passwordless','Webauthn Register Passwordless','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'webauthn-register-passwordless',90),('4ddf08b1-8ec9-415f-918c-2ba3ef3ca89a','UPDATE_PASSWORD','Update Password','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'UPDATE_PASSWORD',57),('5685a9e7-033e-4d23-8b3b-d97b89e43a06','CONFIGURE_RECOVERY_AUTHN_CODES','Recovery Authentication Codes','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'CONFIGURE_RECOVERY_AUTHN_CODES',130),('5885c305-b042-4d0d-9fbd-b40c2585047a','idp_link','Linking Identity Provider','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'idp_link',120),('71dd7221-f948-4099-90bc-b242bffba75c','VERIFY_PROFILE','Verify Profile','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'VERIFY_PROFILE',100),('8c5da72f-0800-4127-9137-8b92b4e8220c','UPDATE_EMAIL','Update Email','faaacb96-1668-4dd7-b538-000594f408e6',0,0,'UPDATE_EMAIL',70),('90b216f4-e0d6-4d35-ab3b-fd111bc30498','delete_credential','Delete Credential','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'delete_credential',110),('c70a28b2-3525-4a0f-8e5b-54b880606bfd','webauthn-register','Webauthn Register','faaacb96-1668-4dd7-b538-000594f408e6',1,0,'webauthn-register',80),('f092c111-af56-423d-9810-3bd4197df06f','TERMS_AND_CONDITIONS','Terms and Conditions','faaacb96-1668-4dd7-b538-000594f408e6',0,0,'TERMS_AND_CONDITIONS',20);
UNLOCK TABLES;

--
-- Dumping data for table `resource_attribute`
--

LOCK TABLES `resource_attribute` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `resource_policy`
--

LOCK TABLES `resource_policy` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `resource_scope`
--

LOCK TABLES `resource_scope` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `resource_server`
--

LOCK TABLES `resource_server` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `resource_server_perm_ticket`
--

LOCK TABLES `resource_server_perm_ticket` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `resource_server_policy`
--

LOCK TABLES `resource_server_policy` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `resource_server_resource`
--

LOCK TABLES `resource_server_resource` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `resource_server_scope`
--

LOCK TABLES `resource_server_scope` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `resource_uris`
--

LOCK TABLES `resource_uris` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `revoked_token`
--

LOCK TABLES `revoked_token` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `role_attribute`
--

LOCK TABLES `role_attribute` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `root_auth_session`
--

LOCK TABLES `root_auth_session` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `scope_mapping`
--

LOCK TABLES `scope_mapping` WRITE;
INSERT INTO `scope_mapping` VALUES ('8c6458b8-7b08-46db-bcfd-f98c4a29714b','8b0cd07f-ad78-4aaf-bca9-dc7e7eb787ae'),('8c6458b8-7b08-46db-bcfd-f98c4a29714b','b73ae2aa-4dbc-49c7-9ede-ef898bcd2ae3');
UNLOCK TABLES;

--
-- Dumping data for table `scope_policy`
--

LOCK TABLES `scope_policy` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `server_config`
--

LOCK TABLES `server_config` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `single_use_object`
--

LOCK TABLES `single_use_object` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `user_attribute`
--

LOCK TABLES `user_attribute` WRITE;
INSERT INTO `user_attribute` VALUES ('is_temporary_admin','true','3e7ffc4a-1e47-4508-b506-4e21d9458ce1','091fd6b1-bab7-45bb-8655-f313fbf623d0',NULL,NULL,NULL);
UNLOCK TABLES;

--
-- Dumping data for table `user_consent`
--

LOCK TABLES `user_consent` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `user_consent_client_scope`
--

LOCK TABLES `user_consent_client_scope` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `user_entity`
--

LOCK TABLES `user_entity` WRITE;
INSERT INTO `user_entity` VALUES ('3e7ffc4a-1e47-4508-b506-4e21d9458ce1',NULL,'9eab54f1-fc01-4dea-85c9-a0d2f16371de',0,1,NULL,NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','admin',1794211597545,NULL,0,1794211597545),('ca629516-55ac-441d-b7f1-4d2e15996a2f',NULL,'ce52637b-8bda-471f-91d6-9fb204d9b04e',0,1,NULL,NULL,NULL,'faaacb96-1668-4dd7-b538-000594f408e6','service-account-_platform',1794211604460,'0060978e-25c0-4f54-9b7b-74dbd36df936',0,1794211604460);
UNLOCK TABLES;

--
-- Dumping data for table `user_federation_config`
--

LOCK TABLES `user_federation_config` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `user_federation_mapper`
--

LOCK TABLES `user_federation_mapper` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `user_federation_mapper_config`
--

LOCK TABLES `user_federation_mapper_config` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `user_federation_provider`
--

LOCK TABLES `user_federation_provider` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `user_group_membership`
--

LOCK TABLES `user_group_membership` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `user_required_action`
--

LOCK TABLES `user_required_action` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `user_role_mapping`
--

LOCK TABLES `user_role_mapping` WRITE;
INSERT INTO `user_role_mapping` VALUES ('6cdd393e-7805-46f1-ba1a-af0021753e4f','3e7ffc4a-1e47-4508-b506-4e21d9458ce1'),('6cdd393e-7805-46f1-ba1a-af0021753e4f','ca629516-55ac-441d-b7f1-4d2e15996a2f'),('d463aee3-b627-4ca9-8d71-c2b46b1364af','3e7ffc4a-1e47-4508-b506-4e21d9458ce1'),('d463aee3-b627-4ca9-8d71-c2b46b1364af','ca629516-55ac-441d-b7f1-4d2e15996a2f');
UNLOCK TABLES;

--
-- Dumping data for table `user_ver_credential`
--

LOCK TABLES `user_ver_credential` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `web_origins`
--

LOCK TABLES `web_origins` WRITE;
INSERT INTO `web_origins` VALUES ('7085a323-1455-4f1b-97f7-bfe1ffa52de8','+');
UNLOCK TABLES;

--
-- Dumping data for table `workflow_state`
--

LOCK TABLES `workflow_state` WRITE;
UNLOCK TABLES;

--
-- Current Database: `platform`
--

USE `platform`;

--
-- Dumping data for table `m_system_config`
--

LOCK TABLES `m_system_config` WRITE;
INSERT INTO `m_system_config` VALUES ('ita.system.ansible.execution_limit','25','Maximum number of movement executions for whole of IT automation','2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('ita.system.menu_export_import.buffer_size','10000','Maximum buffer size of menu Export/import for System default (Used for DB fetch size, file stream read size)','2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('platform.system.audit_log.cleanup_time','04:00','Audit log cleanup time','2026-11-09 17:06:45','dummy','2026-11-09 17:06:45','dummy'),('platform.system.audit_log.download_exp_days','7','Audit log download expiration days','2026-11-09 17:06:45','dummy','2026-11-09 17:06:45','dummy'),('platform.system.audit_log.download_file_limit','100','Audit log download limit','2026-11-09 17:06:45','dummy','2026-11-09 17:06:45','dummy'),('platform.system.audit_log.retention_days','365','Audit log retention days','2026-11-09 17:06:45','dummy','2026-11-09 17:06:45','dummy'),('platform.system.chunk_size','102400','chunk size for upload/download','2026-11-09 17:06:45','dummy','2026-11-09 17:06:45','dummy'),('platform.system.user_export_import.cleanup_time','04:01','User export and bulk import cleanup time','2026-11-09 17:06:46','dummy','2026-11-09 17:06:46','dummy'),('platform.system.user_export_import.exp_days','7','User export and bulk import expiration days','2026-11-09 17:06:46','dummy','2026-11-09 17:06:46','dummy');
UNLOCK TABLES;

--
-- Dumping data for table `t_maintenance_mode`
--

LOCK TABLES `t_maintenance_mode` WRITE;
INSERT INTO `t_maintenance_mode` VALUES ('1','BACKYARD_EXECUTE_STOP','0','2026-11-09 17:06:45.000000',NULL),('2','DATA_UPDATE_STOP','0','2026-11-09 17:06:45.000000',NULL);
UNLOCK TABLES;

--
-- Dumping data for table `t_organization`
--

LOCK TABLES `t_organization` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `t_organization_db`
--

LOCK TABLES `t_organization_db` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `t_organization_plan`
--

LOCK TABLES `t_organization_plan` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `t_plan`
--

LOCK TABLES `t_plan` WRITE;
INSERT INTO `t_plan` VALUES ('_default','_default plan','{\"description\": \"default plan\"}','2026-11-09 17:06:43','system','2026-11-09 17:06:43','system');
UNLOCK TABLES;

--
-- Dumping data for table `t_plan_item`
--

LOCK TABLES `t_plan_item` WRITE;
INSERT INTO `t_plan_item` VALUES ('ita.organization.ansible.execution_limit','{\"description\": \"Maximum number of movement executions for organization default\", \"max\": 1000}','2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('ita.organization.common.maintenance_records_limit','{\"description\": \"Maximum number of maintenance records processing for organization default\", \"max\": 100000}','2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('ita.organization.common.upload_file_size_limit','{\"description\": \"Maximum byte size of upload file for organization default\", \"max\": 107374182400}','2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('ita.organization.menu_export_import.buffer_size','{\"description\": \"Maximum buffer size of menu Export/import for Organization default (Used for DB fetch size, file stream read size)\", \"max\": 10000}','2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('platform.roles','{\"description\": \"Maximum number of roles for organization default\", \"max\": 1000}','2026-11-09 17:06:43','system','2026-11-09 17:06:45','system'),('platform.users','{\"description\": \"Maximum number of users for organization default\", \"max\": 10000}','2026-11-09 17:06:43','system','2026-11-09 17:06:45','system'),('platform.workspaces','{\"description\": \"Maximum number of workspaces for organization default\", \"max\": 1000}','2026-11-09 17:06:43','system','2026-11-09 17:06:45','system');
UNLOCK TABLES;

--
-- Dumping data for table `t_plan_limit`
--

LOCK TABLES `t_plan_limit` WRITE;
INSERT INTO `t_plan_limit` VALUES ('_default','ita.organization.ansible.execution_limit',25,'2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('_default','ita.organization.common.maintenance_records_limit',10000,'2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('_default','ita.organization.common.upload_file_size_limit',104857600,'2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('_default','ita.organization.menu_export_import.buffer_size',1000,'2026-11-09 17:06:55','dummy','2026-11-09 17:06:55','dummy'),('_default','platform.roles',1000,'2026-11-09 17:06:43','system','2026-11-09 17:06:43','system'),('_default','platform.users',10000,'2026-11-09 17:06:43','system','2026-11-09 17:06:43','system'),('_default','platform.workspaces',100,'2026-11-09 17:06:43','system','2026-11-09 17:06:43','system');
UNLOCK TABLES;

--
-- Dumping data for table `t_platform_migration_history`
--

LOCK TABLES `t_platform_migration_history` WRITE;
INSERT INTO `t_platform_migration_history` VALUES (1,'1.3.0','START',NULL,'2026-11-09 17:06:43','2.10.1','2026-11-09 17:06:43','2.10.1'),(2,'1.3.0','SUCCEED',NULL,'2026-11-09 17:06:44','2.10.1','2026-11-09 17:06:44','2.10.1'),(3,'1.5.0','START',NULL,'2026-11-09 17:06:44','2.10.1','2026-11-09 17:06:44','2.10.1'),(4,'1.5.0','SUCCEED',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(5,'1.5.2','START',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(6,'1.5.2','SUCCEED',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(7,'1.6.0','START',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(8,'1.6.0','SUCCEED',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(9,'1.7.0','START',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(10,'1.7.0','SUCCEED',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(11,'1.8.0','START',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(12,'1.8.0','SUCCEED',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(13,'1.8.1','START',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(14,'1.8.1','SUCCEED',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(15,'1.8.100','START',NULL,'2026-11-09 17:06:45','2.10.1','2026-11-09 17:06:45','2.10.1'),(16,'1.8.100','SUCCEED',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(17,'1.9.0','START',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(18,'1.9.0','SUCCEED',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(19,'1.10.0','START',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(20,'1.10.0','SUCCEED',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(21,'1.11.0','START',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(22,'1.11.0','SUCCEED',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(23,'1.12.0','START',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(24,'1.12.0','SUCCEED',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(25,'2.9.0','START',NULL,'2026-11-09 17:06:46','2.10.1','2026-11-09 17:06:46','2.10.1'),(26,'2.9.0','SUCCEED',NULL,'2026-11-09 17:06:47','2.10.1','2026-11-09 17:06:47','2.10.1'),(27,'2.10.0','START',NULL,'2026-11-09 17:06:47','2.10.1','2026-11-09 17:06:47','2.10.1'),(28,'2.10.0','SUCCEED',NULL,'2026-11-09 17:06:47','2.10.1','2026-11-09 17:06:47','2.10.1'),(29,'2.10.1','SUCCEED','Update to System Version','2026-11-09 17:06:47','2.10.1','2026-11-09 17:06:47','2.10.1');
UNLOCK TABLES;

--
-- Dumping data for table `t_platform_private`
--

LOCK TABLES `t_platform_private` WRITE;
INSERT INTO `t_platform_private` VALUES (1,'{\"TOKEN_CHECK_REALM_ID\": \"master\", \"TOKEN_CHECK_CLIENT_CLIENTID\": \"_platform\", \"TOKEN_CHECK_CLIENT_ID\": \"0060978e-25c0-4f54-9b7b-74dbd36df936\", \"TOKEN_CHECK_CLIENT_SECRET\": \"ssTLKTLyDdb3kNve6TdbshIPLQnkjIQs7xP6nY218x9pSQDT23zOEH3y328Z1bhGptBmhgBdDwdlO0p6iSPU6D\", \"API_TOKEN_CLIENT_CLIENTID\": \"_platform-api\", \"API_TOKEN_CLIENT_ID\": \"54c52862-bb56-483f-85dd-e529c984b618\"}','2026-11-09 17:06:44','system','2026-11-09 17:06:44','system');
UNLOCK TABLES;

--
-- Dumping data for table `t_platform_version`
--

LOCK TABLES `t_platform_version` WRITE;
INSERT INTO `t_platform_version` VALUES (1,'2.10.1','2026-11-09 17:05:44','system','2026-11-09 17:06:47','2.10.1');
UNLOCK TABLES;

--
-- Dumping data for table `t_process_queue`
--

LOCK TABLES `t_process_queue` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `t_process_queue_lock`
--

LOCK TABLES `t_process_queue_lock` WRITE;
UNLOCK TABLES;

--
-- Dumping data for table `t_refresh_token`
--

LOCK TABLES `t_refresh_token` WRITE;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-09 17:10:14
SET foreign_key_checks = 1;
